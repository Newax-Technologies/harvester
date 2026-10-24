import pytest
from cryptography.fernet import Fernet

from lead_harvester.config import settings
from lead_harvester.vault_crypto import (
    VaultDecryptionError,
    VaultNotConfiguredError,
    decrypt_secret,
    encrypt_secret,
    fingerprint_secret,
)


@pytest.fixture
def vault_key(monkeypatch):
    key = Fernet.generate_key().decode()
    monkeypatch.setattr(settings, "vault_encryption_key", key)
    return key


def test_encrypt_then_decrypt_round_trips(vault_key):
    ciphertext = encrypt_secret("super-secret-api-key")
    assert ciphertext != "super-secret-api-key"
    assert decrypt_secret(ciphertext) == "super-secret-api-key"


def test_fingerprint_is_deterministic_and_never_equals_the_plaintext(vault_key):
    fp = fingerprint_secret("super-secret-api-key")
    assert fp == fingerprint_secret("super-secret-api-key")
    assert fp != "super-secret-api-key"


def test_fingerprint_differs_for_different_plaintexts(vault_key):
    assert fingerprint_secret("value-a") != fingerprint_secret("value-b")


def test_fingerprint_is_keyed_not_a_bare_hash(monkeypatch):
    # A bare SHA-256 would give the same fingerprint for the same
    # plaintext regardless of VAULT_ENCRYPTION_KEY -- letting anyone who
    # reads the fingerprint column brute-force a low-entropy secret with
    # a fast hash and no knowledge of the key at all. Keyed (HMAC) means
    # the same plaintext under two different keys must fingerprint
    # differently.
    monkeypatch.setattr(settings, "vault_encryption_key", Fernet.generate_key().decode())
    fp_under_key_a = fingerprint_secret("super-secret-api-key")

    monkeypatch.setattr(settings, "vault_encryption_key", Fernet.generate_key().decode())
    fp_under_key_b = fingerprint_secret("super-secret-api-key")

    assert fp_under_key_a != fp_under_key_b


def test_fingerprint_raises_when_no_key_configured(monkeypatch):
    monkeypatch.setattr(settings, "vault_encryption_key", "")
    with pytest.raises(VaultNotConfiguredError):
        fingerprint_secret("anything")


def test_encrypt_raises_when_no_key_configured(monkeypatch):
    monkeypatch.setattr(settings, "vault_encryption_key", "")
    with pytest.raises(VaultNotConfiguredError):
        encrypt_secret("anything")


def test_encrypt_raises_for_a_malformed_key(monkeypatch):
    monkeypatch.setattr(settings, "vault_encryption_key", "not-a-valid-fernet-key")
    with pytest.raises(VaultNotConfiguredError):
        encrypt_secret("anything")


def test_decrypt_raises_a_clean_error_for_the_wrong_key(monkeypatch):
    monkeypatch.setattr(settings, "vault_encryption_key", Fernet.generate_key().decode())
    ciphertext = encrypt_secret("super-secret-api-key")

    monkeypatch.setattr(settings, "vault_encryption_key", Fernet.generate_key().decode())
    with pytest.raises(VaultDecryptionError):
        decrypt_secret(ciphertext)
