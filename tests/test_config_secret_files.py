from pathlib import Path

from lead_harvester.config import Settings


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_secrets_file_overrides_general_dotenv(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("GOOGLE_PLACES_API_KEY", raising=False)
    monkeypatch.delenv("YANDEX_MAPS_API_KEY", raising=False)

    general_env = _write(
        tmp_path / ".env",
        "GOOGLE_PLACES_API_KEY=general-google\nYANDEX_MAPS_API_KEY=general-yandex\n",
    )
    secrets_env = _write(
        tmp_path / ".env.secrets",
        "GOOGLE_PLACES_API_KEY=secret-google\nYANDEX_MAPS_API_KEY=secret-yandex\n",
    )

    settings = Settings(_env_file=(general_env, secrets_env))

    assert settings.google_places_api_key == "secret-google"
    assert settings.yandex_maps_api_key == "secret-yandex"


def test_process_environment_overrides_both_local_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_PLACES_API_KEY", "deployment-google")

    general_env = _write(tmp_path / ".env", "GOOGLE_PLACES_API_KEY=general-google\n")
    secrets_env = _write(tmp_path / ".env.secrets", "GOOGLE_PLACES_API_KEY=secret-google\n")

    settings = Settings(_env_file=(general_env, secrets_env))

    assert settings.google_places_api_key == "deployment-google"
