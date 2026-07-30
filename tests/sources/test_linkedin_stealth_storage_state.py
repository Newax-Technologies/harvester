import json

from lead_harvester.sources.linkedin_stealth import (
    _load_storage_state,
    _save_storage_state,
    _storage_path,
)


def test_storage_path_respects_configured_sessions_dir(tmp_path):
    path = _storage_path("burner_01", str(tmp_path))
    assert path.parent == tmp_path


def test_save_and_load_storage_state_round_trips_within_sessions_dir(tmp_path):
    state = {"localStorage": {"foo": "bar"}}
    _save_storage_state("burner_01", state, str(tmp_path))

    saved_path = tmp_path / "burner_01_storage.json"
    assert saved_path.exists()
    assert json.loads(saved_path.read_text()) == state

    loaded = _load_storage_state("burner_01", str(tmp_path))
    assert loaded == state


def test_save_storage_state_never_writes_outside_the_configured_directory(tmp_path, monkeypatch):
    # Regression test: _storage_path previously hardcoded Path("sessions")
    # regardless of the sessions_dir a caller configured, so storage state
    # silently leaked into a repo-relative "sessions/" directory (visible
    # as untracked files after running the suite) even when a crawler was
    # constructed with sessions_dir=str(tmp_path) -- exactly what the
    # existing budget/partial-results tests already pass.
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    isolated_sessions_dir = tmp_path / "isolated"
    isolated_sessions_dir.mkdir()

    _save_storage_state("burner_01", {"localStorage": {}}, str(isolated_sessions_dir))

    assert not (cwd / "sessions").exists()
    assert (isolated_sessions_dir / "burner_01_storage.json").exists()
