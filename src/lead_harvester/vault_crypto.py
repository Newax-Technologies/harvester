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

from cryptography.fernet import Fernet, InvalidToken

from lead_harvester.config import settings

# PBKDF2 iteration count for fingerprint_secret() -- high enough to be
# genuinely expensive per guess (OWASP's 2023 minimum for
# PBKDF2-HMAC-SHA256 is 600,000; this trades some of that down since a
# vault fingerprint isn't checked on every login the way a password hash
# is, and the test suite calls this function often), while still several
# orders of magnitude past what a bare hash or a single HMAC round costs.
_FINGERPRINT_ITERATIONS = 100_000


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
    A PBKDF2-HMAC-SHA256 digest of the plaintext, keyed by
    VAULT_ENCRYPTION_KEY -- lets an operator confirm "is this the
    credential I think it is" (e.g. compare against a known value) or
    spot that two stored credentials share a value, without ever
    decrypting either one. Never used to recover plaintext.

    Deliberately not a bare hash, and not just a keyed-but-fast HMAC
    either: a plain SHA-256 of the plaintext would let anyone who ever
    reads the fingerprint column (a DB leak, a log line) run an offline
    dictionary/brute-force search for a low-entropy secret -- a
    human-chosen password, say, as opposed to a random API key -- using
    nothing but a fast hash function. A single round of keyed HMAC-SHA256
    closes that specific hole (an attacker without VAULT_ENCRYPTION_KEY
    can't compute matching fingerprints at all) but is still cheap enough
    to brute-force quickly if the key AND the fingerprint column are ever
    compromised together -- a real risk for this module's app-level key
    (see the module docstring), which lives in the same process as the
    data it protects, not a separately-secured KMS. PBKDF2's iteration
    count (_FINGERPRINT_ITERATIONS) makes each guess expensive even in
    that combined-compromise case, which is what CodeQL's "insecure for
    password hashing... not a computationally expensive hash function"
    rule is actually asking for. Still fully deterministic for a fixed
    key + plaintext, which is what fingerprint comparison needs. Raises
    VaultNotConfiguredError under the same condition as
    encrypt_secret/decrypt_secret.
    """
    key = _require_key()
    return hashlib.pbkdf2_hmac(
        "sha256", plaintext.encode("utf-8"), key.encode("utf-8"), _FINGERPRINT_ITERATIONS
    ).hex()
