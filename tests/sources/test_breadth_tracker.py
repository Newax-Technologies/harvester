from datetime import UTC, datetime

from lead_harvester.sources.breadth_tracker import (
    MAX_BREADTH_PER_VERTICAL_CITY_30D,
    BreadthTracker,
)


def _tracker(tmp_path) -> BreadthTracker:
    return BreadthTracker(log_path=tmp_path / "breadth_log.json")


def test_assign_partitions_allocates_work_below_the_breadth_ceiling(tmp_path):
    bt = _tracker(tmp_path)

    result = bt.assign_partitions(
        ["https://linkedin.com/in/alice"],
        ["burner_01"],
        {"burner_01": 5},
        vertical="school_principals",
        target_city="karachi",
    )

    assert result == {"burner_01": ["https://linkedin.com/in/alice"]}


def test_assign_partitions_stops_new_work_once_breadth_ceiling_reached(tmp_path):
    # is_breadth_exceeded/needs_noise_visit were never called anywhere in
    # account_farm.py -- assign_partitions only deduped exact previously-
    # visited URLs and capped per-account counts, so the advertised
    # 40-profile/30-day ceiling stayed inert even once visits were being
    # recorded. Once a (vertical, city) combination has hit the ceiling,
    # no further URLs targeting it -- new OR previously-partitioned
    # backlog -- may be handed out to any account.
    bt = _tracker(tmp_path)
    for i in range(MAX_BREADTH_PER_VERTICAL_CITY_30D):
        bt.record_visit(
            "burner_01",
            f"https://linkedin.com/in/already-visited-{i}",
            industry="school_principals",
            city="karachi",
        )

    result = bt.assign_partitions(
        ["https://linkedin.com/in/new-target"],
        ["burner_01", "burner_02"],
        {"burner_01": 10, "burner_02": 10},
        vertical="school_principals",
        target_city="karachi",
    )

    assert result == {"burner_01": [], "burner_02": []}


def test_assign_partitions_ceiling_is_scoped_per_vertical_and_city(tmp_path):
    # A different vertical (or city) combination must not be blocked by an
    # unrelated combination's own saturation.
    bt = _tracker(tmp_path)
    for i in range(MAX_BREADTH_PER_VERTICAL_CITY_30D):
        bt.record_visit(
            "burner_01",
            f"https://linkedin.com/in/saturated-{i}",
            industry="school_principals",
            city="karachi",
        )

    result = bt.assign_partitions(
        ["https://linkedin.com/in/new-target"],
        ["burner_01"],
        {"burner_01": 10},
        vertical="school_principals",
        target_city="lahore",
    )

    assert result == {"burner_01": ["https://linkedin.com/in/new-target"]}


def test_assign_partitions_injects_noise_visit_when_due(tmp_path):
    # needs_noise_visit was never actually wired into assign_partitions --
    # an account due for a noise visit (every 4th target visit) never
    # actually got one, since there was no mechanism to substitute an
    # off-target URL into its work queue.
    bt = _tracker(tmp_path)
    today = datetime.now(UTC).date().isoformat()
    for i in range(4):
        bt._data.setdefault("visits", []).append(
            {
                "account_id": "burner_01",
                "url": f"https://linkedin.com/in/target-{i}",
                "industry": "school_principals",
                "city": "karachi",
                "date": today,
            }
        )
    assert bt.needs_noise_visit("burner_01")

    result = bt.assign_partitions(
        ["https://linkedin.com/in/next-target"],
        ["burner_01"],
        {"burner_01": 5},
        vertical="school_principals",
        target_city="karachi",
        noise_urls=["https://linkedin.com/in/noise-a", "https://linkedin.com/in/noise-b"],
    )

    assert result["burner_01"][0] == "https://linkedin.com/in/noise-a"
    assert "https://linkedin.com/in/next-target" in result["burner_01"]

    # The chosen noise URL is remembered so the caller can record it with
    # industry="noise" instead of the batch's real vertical.
    assert bt.consume_noise_marker("burner_01", "https://linkedin.com/in/noise-a")
    # Consuming it clears the marker -- a second consume for the same URL
    # must not still report it as pending.
    assert not bt.consume_noise_marker("burner_01", "https://linkedin.com/in/noise-a")


def test_assign_partitions_does_not_double_assign_the_same_noise_url(tmp_path):
    bt = _tracker(tmp_path)
    today = datetime.now(UTC).date().isoformat()
    for acc in ("burner_01", "burner_02"):
        for i in range(4):
            bt._data.setdefault("visits", []).append(
                {
                    "account_id": acc,
                    "url": f"https://linkedin.com/in/{acc}-target-{i}",
                    "industry": "school_principals",
                    "city": "karachi",
                    "date": today,
                }
            )

    result = bt.assign_partitions(
        ["https://linkedin.com/in/target-a", "https://linkedin.com/in/target-b"],
        ["burner_01", "burner_02"],
        {"burner_01": 5, "burner_02": 5},
        vertical="school_principals",
        target_city="karachi",
        noise_urls=["https://linkedin.com/in/only-one-noise-profile"],
    )

    noise_recipients = [
        acc
        for acc in ("burner_01", "burner_02")
        if "https://linkedin.com/in/only-one-noise-profile" in result[acc]
    ]
    assert len(noise_recipients) == 1


def test_consume_noise_marker_returns_false_for_unmarked_url(tmp_path):
    bt = _tracker(tmp_path)
    assert not bt.consume_noise_marker("burner_01", "https://linkedin.com/in/never-flagged")
