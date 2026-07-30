import contextlib
import multiprocessing
import threading
import time
from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.source import RawSourceRecord, SourceType
from lead_harvester.sources.account_farm import AccountFarm, AccountResult, _drain_result_queue
from lead_harvester.sources.breadth_tracker import BreadthTracker


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


def _put_large_payload(result_queue: multiprocessing.Queue) -> None:
    # A payload comfortably larger than a typical OS pipe buffer (~64KB on
    # Linux) -- large enough that queue.put() blocks until something reads
    # from the pipe, reproducing the condition under which draining only
    # after p.join() would deadlock.
    result_queue.put(
        {
            "account_id": "big_account",
            "profiles_scraped": 1,
            "errors": [],
            "city": "Karachi",
            "warmup_phase": 5,
            "profiles": [{"raw_html_snippet": "x" * 5_000_000}],
        }
    )


@pytest.mark.asyncio
async def test_persist_profiles_writes_raw_source_records(db_session):
    # _run_account_worker previously returned only a bare profiles_scraped
    # count to the parent process -- the actual scraped profile data was
    # discarded, so a "successful" farm run left nothing in the database
    # for linkedin-research to process. _persist_profiles is what now
    # writes every worker's harvested profiles to RawSourceRecord.
    results = [
        AccountResult(
            account_id="burner_01",
            profiles_scraped=2,
            city="Karachi",
            warmup_phase=3,
            profiles=[
                {"profile_url": "https://linkedin.com/in/alice", "full_name": "Alice A"},
                {"profile_url": "https://linkedin.com/in/bob", "full_name": "Bob B"},
            ],
        ),
        AccountResult(
            account_id="burner_02",
            profiles_scraped=0,
            errors=["No session saved"],
            profiles=[],
        ),
    ]

    farm = AccountFarm(accounts=["burner_01", "burner_02"])

    with patch(
        "lead_harvester.sources.account_farm.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await farm._persist_profiles(results)

    records = (
        (
            await db_session.execute(
                select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.LINKEDIN)
            )
        )
        .scalars()
        .all()
    )
    assert {r.source_id for r in records} == {
        "https://linkedin.com/in/alice",
        "https://linkedin.com/in/bob",
    }
    assert {r.normalized_name for r in records} == {"Alice A", "Bob B"}


@pytest.mark.asyncio
async def test_persist_profiles_no_ops_when_nothing_scraped(db_session):
    results = [AccountResult(account_id="burner_01", profiles_scraped=0, profiles=[])]
    farm = AccountFarm(accounts=["burner_01"])

    with patch(
        "lead_harvester.sources.account_farm.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await farm._persist_profiles(results)

    count = await db_session.scalar(
        select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.LINKEDIN)
    )
    assert count is None


def test_drain_result_queue_collects_items_while_producer_still_running():
    # The drainer must pick up results as they arrive, not only once every
    # producer has finished -- proves AccountFarm.run() no longer needs to
    # wait for every p.join() before consuming from result_queue.
    result_queue: multiprocessing.Queue = multiprocessing.Queue()
    results: list[AccountResult] = []
    stop_event = threading.Event()
    drainer = threading.Thread(target=_drain_result_queue, args=(result_queue, results, stop_event))
    drainer.start()

    def producer():
        for i in range(3):
            result_queue.put(
                {
                    "account_id": f"acc_{i}",
                    "profiles_scraped": i,
                    "errors": [],
                    "city": "",
                    "warmup_phase": 0,
                    "profiles": [],
                }
            )
            time.sleep(0.2)

    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    producer_thread.join()

    # Give the drainer a moment to pick up the last item before stopping it.
    time.sleep(0.6)
    stop_event.set()
    drainer.join(timeout=5)

    assert not drainer.is_alive()
    assert {r.account_id for r in results} == {"acc_0", "acc_1", "acc_2"}


def test_drain_result_queue_prevents_deadlock_on_large_payload():
    # Regression test for the reported deadlock: previously
    # AccountFarm.run() only read from result_queue after every p.join()
    # returned. A worker whose result dict is larger than the OS pipe
    # buffer blocks inside queue.put() until something reads from the
    # queue -- so the parent's p.join() and the worker's put() waited on
    # each other forever (until the 7200s timeout terminated the worker
    # and discarded its data). Draining concurrently via a background
    # thread means the worker's put() unblocks immediately and join()
    # returns promptly.
    result_queue: multiprocessing.Queue = multiprocessing.Queue()
    results: list[AccountResult] = []
    stop_event = threading.Event()
    drainer = threading.Thread(target=_drain_result_queue, args=(result_queue, results, stop_event))
    drainer.start()

    proc = multiprocessing.Process(target=_put_large_payload, args=(result_queue,))
    proc.start()
    proc.join(timeout=30)
    assert not proc.is_alive(), "worker deadlocked writing a large payload to the queue"

    stop_event.set()
    drainer.join(timeout=5)

    assert len(results) == 1
    assert results[0].account_id == "big_account"


def test_record_farm_visits_logs_every_scraped_profile(tmp_path):
    # No caller anywhere recorded a visit before this -- assign_partitions'
    # own "not in visited_urls" exclusion, the 30-day breadth ceiling, and
    # the noise-injection scheduling all read the same visits list, so
    # nothing ever writing to it left every one of those checks
    # permanently inert (the farm could keep re-visiting the exact same
    # URLs indefinitely).
    bt = BreadthTracker(log_path=tmp_path / "breadth_log.json")
    results = [
        AccountResult(
            account_id="burner_01",
            profiles_scraped=2,
            profiles=[
                {"profile_url": "https://linkedin.com/in/alice", "location": "Karachi, Pakistan"},
                {"profile_url": "https://linkedin.com/in/bob"},
            ],
        ),
        AccountResult(
            account_id="burner_02", profiles_scraped=0, errors=["No session"], profiles=[]
        ),
    ]

    AccountFarm._record_farm_visits(bt, results)

    visited_urls = {v["url"] for v in bt._data["visits"]}
    assert visited_urls == {"https://linkedin.com/in/alice", "https://linkedin.com/in/bob"}

    alice_visit = next(v for v in bt._data["visits"] if v["url"].endswith("alice"))
    assert alice_visit["account_id"] == "burner_01"
    assert alice_visit["city"] == "karachi, pakistan"

    bob_visit = next(v for v in bt._data["visits"] if v["url"].endswith("bob"))
    assert bob_visit["city"] == "unknown"
