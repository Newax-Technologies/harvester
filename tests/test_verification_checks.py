import uuid
from datetime import UTC, datetime, timedelta

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.verification import FlagType
from lead_harvester.verification.checks import (
    check_confidence_drift,
    check_conflicting_canonical_name,
    check_stale_evidence,
)
from lead_harvester.verification.confidence import confidence_for_source_count


def _institution(**overrides) -> CanonicalInstitution:
    defaults = {"canonical_name": "Riverside Academy", "confidence_score": 10.0}
    defaults.update(overrides)
    return CanonicalInstitution(**defaults)


def _provenance(field_name: str, value, *, created_at=None) -> FieldProvenance:
    return FieldProvenance(
        canonical_id=uuid.uuid4(),
        raw_record_id=uuid.uuid4(),
        field_name=field_name,
        asserted_value=value,
        created_at=created_at or datetime.now(UTC),
    )


def test_confidence_drift_none_when_stored_matches_expected():
    institution = _institution(confidence_score=confidence_for_source_count(3))
    assert check_confidence_drift(institution, 3) is None


def test_confidence_drift_flagged_when_stored_diverges():
    institution = _institution(confidence_score=10.0)
    result = check_confidence_drift(institution, 5)
    assert result is not None
    assert result.flag_type == FlagType.CONFIDENCE_DRIFT
    assert result.details["stored"] == 10.0
    assert result.details["expected"] == confidence_for_source_count(5)


def test_stale_evidence_none_when_recent():
    institution = _institution()
    result = check_stale_evidence(
        institution,
        datetime.now(UTC) - timedelta(days=1),
        now=datetime.now(UTC),
        freshness_days=90,
    )
    assert result is None


def test_stale_evidence_flagged_when_past_the_window():
    institution = _institution()
    result = check_stale_evidence(
        institution,
        datetime.now(UTC) - timedelta(days=100),
        now=datetime.now(UTC),
        freshness_days=90,
    )
    assert result is not None
    assert result.flag_type == FlagType.STALE_EVIDENCE
    assert result.details["age_days"] == 100


def test_stale_evidence_flagged_when_never_recorded():
    institution = _institution()
    result = check_stale_evidence(institution, None, now=datetime.now(UTC), freshness_days=90)
    assert result is not None
    assert result.details["latest_evidence_at"] is None
    assert result.details["age_days"] is None


def test_conflicting_canonical_name_none_for_a_single_source():
    institution = _institution()
    provenance = [_provenance("canonical_name", "Riverside Academy")]
    assert check_conflicting_canonical_name(institution, provenance) is None


def test_conflicting_canonical_name_none_when_sources_agree_after_normalization():
    institution = _institution()
    provenance = [
        _provenance("canonical_name", "Riverside Academy"),
        _provenance("canonical_name", "riverside academy"),
        _provenance("canonical_name", "Riverside, Academy"),
    ]
    assert check_conflicting_canonical_name(institution, provenance) is None


def test_conflicting_canonical_name_flagged_when_sources_genuinely_disagree():
    institution = _institution()
    provenance = [
        _provenance("canonical_name", "Riverside Academy"),
        _provenance("canonical_name", "Lakeside Academy"),
    ]
    result = check_conflicting_canonical_name(institution, provenance)
    assert result is not None
    assert result.flag_type == FlagType.CONFLICTING_FIELD
    assert result.field_name == "canonical_name"
    assert set(result.details["values"]) == {"Riverside Academy", "Lakeside Academy"}
