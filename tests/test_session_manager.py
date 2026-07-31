import json
import threading
from datetime import UTC, datetime, timedelta

from lead_harvester.sources.session_manager import SessionManager


def test_actions_taken_today_sums_only_todays_entries(tmp_path):
    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_01", [{"name": "x", "value": "y"}], first_login=True)

    today = datetime.now(UTC).date().isoformat()
    yesterday = (datetime.now(UTC).date() - timedelta(days=1)).isoformat()

    path = tmp_path / "burner_01.json"
    payload = json.loads(path.read_text())
    payload["run_log"] = [
        {"date": yesterday, "actions": {"message": 10}},
        {"date": today, "actions": {"message": 2}},
        {"date": today, "actions": {"message": 1, "profile_view": 3}},
    ]
    path.write_text(json.dumps(payload))

    totals = sm.actions_taken_today("burner_01")

    assert totals == {"message": 3, "profile_view": 3}


def test_actions_taken_today_empty_for_no_session(tmp_path):
    sm = SessionManager(tmp_path)
    assert sm.actions_taken_today("nobody") == {}


def test_reserve_action_never_over_grants_under_real_concurrency(tmp_path):
    # Two genuinely concurrent reserve_action calls (separate threads, each
    # opening its own file handle and flock) for the same account must
    # never collectively grant more than the daily limit -- proves the
    # fcntl.flock-guarded read-modify-write actually serializes instead of
    # each thread reading the same stale "0 used" snapshot.
    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_03", [{"name": "x", "value": "y"}], first_login=True)
    path = tmp_path / "burner_03.json"
    payload = json.loads(path.read_text())
    payload["warmup_started_at"] = (datetime.now(UTC).date() - timedelta(days=18)).isoformat()
    path.write_text(json.dumps(payload))

    # Week 3 limit is 2 messages/day.
    results: list[int] = []
    barrier = threading.Barrier(2)

    def worker():
        barrier.wait()
        results.append(sm.reserve_action("burner_03", "message", 2))

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sum(results) == 2
    assert sm.actions_taken_today("burner_03") == {"message": 2}


def test_release_action_gives_back_unused_reservation(tmp_path):
    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_04", [{"name": "x", "value": "y"}], first_login=True)
    path = tmp_path / "burner_04.json"
    payload = json.loads(path.read_text())
    payload["warmup_started_at"] = (datetime.now(UTC).date() - timedelta(days=18)).isoformat()
    path.write_text(json.dumps(payload))

    granted = sm.reserve_action("burner_04", "message", 2)
    assert granted == 2
    sm.release_action("burner_04", "message", 1)

    assert sm.actions_taken_today("burner_04") == {"message": 1}
    assert sm.reserve_action("burner_04", "message", 5) == 1


def test_captcha_cooldown_remaining_zero_when_no_challenge_recorded(tmp_path):
    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_05", [{"name": "x", "value": "y"}], first_login=True)

    assert sm.captcha_cooldown_remaining("burner_05") == timedelta(0)


def test_captcha_cooldown_remaining_reflects_elapsed_real_time(tmp_path):
    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_06", [{"name": "x", "value": "y"}], first_login=True)

    sm.record_captcha_challenge("burner_06")
    remaining = sm.captcha_cooldown_remaining("burner_06")
    assert timedelta(hours=23, minutes=59) < remaining <= timedelta(hours=24)

    # Back-date the challenge to 25 hours ago -- cooldown must have expired.
    path = tmp_path / "burner_06.json"
    payload = json.loads(path.read_text())
    payload["last_captcha_at"] = (datetime.now(UTC) - timedelta(hours=25)).isoformat()
    path.write_text(json.dumps(payload))

    assert sm.captcha_cooldown_remaining("burner_06") == timedelta(0)


def test_save_cookies_preserves_last_captcha_at(tmp_path):
    # save_cookies previously reconstructed the whole session payload from
    # scratch, preserving only warmup_started_at/run_log -- called from the
    # crawler's own cleanup finally-block after a CAPTCHA-triggered abort,
    # it silently overwrote the session file and dropped the
    # last_captcha_at that record_captcha_challenge had JUST written
    # moments earlier in that same run, so the very next invocation saw no
    # cooldown recorded at all and reused the flagged account immediately.
    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_07", [{"name": "x", "value": "y"}], first_login=True)

    sm.record_captcha_challenge("burner_07")
    assert sm.captcha_cooldown_remaining("burner_07") > timedelta(0)

    # Simulates the crawler's cleanup finally-block re-saving cookies after
    # the CAPTCHA-triggered abort.
    sm.save_cookies("burner_07", [{"name": "x", "value": "z"}])

    assert sm.captcha_cooldown_remaining("burner_07") > timedelta(0)
