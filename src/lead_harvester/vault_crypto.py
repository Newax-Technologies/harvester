"""
App-level envelope encryption for services/credential_vault_service.py --
docs/ROADMAP.md Module 09 / docs/delivery/
agency-intelligence-implementation-sequence.md Slice 2.1.

A single symmetric key (Settings.vault_encryption_key, a Fernet key from
VAULT_ENCRYPTION_KEY) encrypts every vaulted credential's plaintext value
before it is written to the database -- the database only ever holds
ciphertext plus a one-way fingerprint, never plaintext. This is
app-level, not an external KMS/Vault integration: the key lives in this
process's environment, not a separate key-management service. That is a
real, deliberate trade-off (see the Gate 2 decision in this conversation)
-- weaker than a real HSM/KMS boundary, but requires no external
infrastructure this environment can provision.

decrypt_secret() is the only function in this codebase that recovers
plaintext from a vaulted value -- see credential_vault_service.py's
retrieve_plaintext_for_use() for the one sanctioned caller.
"""

from __future__ import annotations

import hashlib
import hmac

from cryptography.fernet import Fernet, InvalidToken

from lead_harvester.config import settings


class VaultNotConfiguredError(RuntimeError):
    """Raised when VAULT_ENCRYPTION_KEY is unset or not a valid Fernet key."""


class VaultDecryptionError(RuntimeError):
    """Raised when ciphertext can't be decrypted with the configured key (wrong key, corrupted value)."""


def _require_key() -> str:
    key = settings.vault_encryption_key
    if not key:
        raise VaultNotConfiguredError(
            "VAULT_ENCRYPTION_KEY is not set -- generate one with "
            '`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` '
            "and set it before storing or reading vaulted credentials."
        )
    return key


def _fernet() -> Fernet:
    key = _require_key()
    try:
        return Fernet(key.encode("utf-8"))
    except (ValueError, TypeError) as e:
        raise VaultNotConfiguredError(
            "VAULT_ENCRYPTION_KEY is not a valid Fernet key (must be 32 url-safe base64-encoded bytes)."
        ) from e


def encrypt_secret(plaintext: str) -> str:
    return _fernet().encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_secret(ciphertext: str) -> str:
    try:
        return _fernet().decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except InvalidToken as e:
        raise VaultDecryptionError(
            "Vaulted value could not be decrypted -- wrong VAULT_ENCRYPTION_KEY, or the value is corrupted."
        ) from e


def fingerprint_secret(plaintext: str) -> str:
    """
    A keyed HMAC-SHA256 digest of the plaintext, keyed by
    VAULT_ENCRYPTION_KEY -- lets an operator confirm "is this the
    credential I think it is" (e.g. compare against a known value) or
    spot that two stored credentials share a value, without ever
    decrypting either one. Never used to recover plaintext.

    Keyed, not a bare hash: a plain SHA-256 of the plaintext would let
    anyone who ever reads the fingerprint column (a DB leak, a log line)
    run an offline dictionary/brute-force search for a low-entropy
    secret -- a human-chosen password, say, as opposed to a random API
    key -- using nothing but a fast hash function and no knowledge of
    VAULT_ENCRYPTION_KEY at all (CodeQL flags exactly this: an unsalted
    fast hash on sensitive data). Keying the digest with the same secret
    that protects the ciphertext means computing a matching fingerprint
    for a guess also requires that key, closing the oracle. Raises
    VaultNotConfiguredError under the same condition as
    encrypt_secret/decrypt_secret.
    """
    key = _require_key()
    return hmac.new(key.encode("utf-8"), plaintext.encode("utf-8"), hashlib.sha256).hexdigest()
