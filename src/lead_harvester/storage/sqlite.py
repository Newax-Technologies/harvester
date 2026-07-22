from __future__ import annotations

import sqlite3
from typing import Iterable

from ..entities.institution import Institution
from ..entities.branch import Branch
from ..entities.contact import ContactPoint
from ..entities.signal import OpportunitySignal

SCHEMA = """
CREATE TABLE IF NOT EXISTS institutions (
    id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    institution_type TEXT NOT NULL DEFAULT '',
    ownership_type TEXT NOT NULL DEFAULT '',
    website TEXT NOT NULL DEFAULT '',
    domain TEXT NOT NULL DEFAULT '',
    primary_phone TEXT NOT NULL DEFAULT '',
    primary_email TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'OPERATIONAL',
    estimated_size TEXT NOT NULL DEFAULT '',
    estimated_value_tier TEXT NOT NULL DEFAULT '',
    confidence REAL NOT NULL DEFAULT 0.0,
    discovered_at TEXT NOT NULL,
    raw_data TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS branches (
    id TEXT PRIMARY KEY,
    institution_id TEXT NOT NULL,
    branch_name TEXT NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    city TEXT NOT NULL DEFAULT '',
    area TEXT NOT NULL DEFAULT '',
    latitude REAL NOT NULL DEFAULT 0.0,
    longitude REAL NOT NULL DEFAULT 0.0,
    map_provider_ids TEXT NOT NULL DEFAULT '{}',
    phones TEXT NOT NULL DEFAULT '[]',
    opening_hours TEXT NOT NULL DEFAULT '',
    FOREIGN KEY(institution_id) REFERENCES institutions(id)
);

CREATE TABLE IF NOT EXISTS contact_points (
    id TEXT PRIMARY KEY,
    institution_id TEXT NOT NULL,
    person_name TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL DEFAULT '',
    email TEXT NOT NULL DEFAULT '',
    phone TEXT NOT NULL DEFAULT '',
    whatsapp TEXT NOT NULL DEFAULT '',
    contact_form_url TEXT NOT NULL DEFAULT '',
    telegram_username TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT '',
    publicly_listed INTEGER NOT NULL DEFAULT 0,
    verified_at TEXT NOT NULL DEFAULT '',
    FOREIGN KEY(institution_id) REFERENCES institutions(id)
);

CREATE TABLE IF NOT EXISTS opportunity_signals (
    id TEXT PRIMARY KEY,
    institution_id TEXT NOT NULL,
    signal_type TEXT NOT NULL DEFAULT '',
    signal_text TEXT NOT NULL DEFAULT '',
    source_url TEXT NOT NULL DEFAULT '',
    detected_at TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.0,
    freshness INTEGER NOT NULL DEFAULT 0,
    commercial_relevance REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY(institution_id) REFERENCES institutions(id)
);

CREATE INDEX IF NOT EXISTS idx_inst_domain ON institutions(domain);
CREATE INDEX IF NOT EXISTS idx_branch_inst ON branches(institution_id);
CREATE INDEX IF NOT EXISTS idx_contact_inst ON contact_points(institution_id);
CREATE INDEX IF NOT EXISTS idx_signal_inst ON opportunity_signals(institution_id);
"""

INST_COLS = ["id", "canonical_name", "institution_type", "ownership_type", "website", "domain", "primary_phone", "primary_email", "status", "estimated_size", "estimated_value_tier", "confidence", "discovered_at", "raw_data"]
BRANCH_COLS = ["id", "institution_id", "branch_name", "address", "city", "area", "latitude", "longitude", "map_provider_ids", "phones", "opening_hours"]
CONTACT_COLS = ["id", "institution_id", "person_name", "role", "email", "phone", "whatsapp", "contact_form_url", "telegram_username", "source", "publicly_listed", "verified_at"]
SIGNAL_COLS = ["id", "institution_id", "signal_type", "signal_text", "source_url", "detected_at", "confidence", "freshness", "commercial_relevance"]

class SQLiteStore:
    def __init__(self, path: str):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.connection.executescript(SCHEMA)

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteStore":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:  # type: ignore
        self.close()

    def _upsert(self, table: str, columns: list[str], data_tuple: tuple) -> None:
        placeholders = ", ".join("?" for _ in columns)
        updates = ", ".join(f"{col}=excluded.{col}" for col in columns if col != "id")
        query = f"""
            INSERT INTO {table} ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(id) DO UPDATE SET {updates}
        """
        self.connection.execute(query, data_tuple)

    def upsert_institution(self, institution: Institution) -> None:
        self._upsert("institutions", INST_COLS, institution.to_db_tuple())
        self.connection.commit()

    def upsert_branch(self, branch: Branch) -> None:
        self._upsert("branches", BRANCH_COLS, branch.to_db_tuple())
        self.connection.commit()

    def upsert_contact_point(self, contact: ContactPoint) -> None:
        self._upsert("contact_points", CONTACT_COLS, contact.to_db_tuple())
        self.connection.commit()

    def upsert_opportunity_signal(self, signal: OpportunitySignal) -> None:
        self._upsert("opportunity_signals", SIGNAL_COLS, signal.to_db_tuple())
        self.connection.commit()
