from unittest.mock import patch

import pytest

from lead_harvester.sources.human_emulator import session_start_delay_seconds


@pytest.mark.parametrize("jitter_draw", [45, 44, 30, -45, -44, -30, 0])
def test_session_start_delay_seconds_handles_extreme_jitter(jitter_draw):
    # preferred_start_jitter is drawn from range(10, 45) (device_profile.py),
    # so 30 + jitter can be as high as 75 or as low as -15 -- both invalid
    # for datetime.replace(minute=...), which previously raised ValueError
    # before the crawler ever opened a browser. Forcing random.randint to
    # return the extreme ends of the jitter range reproduces every
    # boundary case.
    with patch("lead_harvester.sources.human_emulator.random.randint", return_value=jitter_draw):
        delay = session_start_delay_seconds(preferred_hour=14, jitter_minutes=45)

    assert isinstance(delay, float)
    assert delay >= 0.0
