import json
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
