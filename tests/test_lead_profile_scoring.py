from datetime import UTC, datetime, timedelta

from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus
from lead_harvester.models.research import FindingType, ResearchFinding
from lead_harvester.profiles.scoring import compute_lead_score


def _institution(**overrides) -> CanonicalInstitution:
    defaults = {
        "canonical_name": "Riverside Academy",
        "institution_type": "school",
        "website": "https://riverside.edu",
        "confidence_score": 90.0,  # 0-100 scale -- see verification/confidence.py
    }
    defaults.update(overrides)
    return CanonicalInstitution(**defaults)


def _finding(key: str, value, *, created_at=None) -> ResearchFinding:
    return ResearchFinding(
        institution_id=None,
        job_id=None,
        finding_type=FindingType.INFERENCE,
        finding_key=key,
        finding_value=value,
        created_at=created_at or datetime.now(UTC),
    )


def test_bare_institution_with_no_evidence_scores_low():
    institution = _institution(website=None, institution_type="", confidence_score=0.0)

    result = compute_lead_score(institution, [], [], None, [])

    assert result.overall_score == 0
    assert result.has_phone is False
    assert result.has_email is False
    assert result.has_named_contact is False
    assert result.evidence_count == 0


def test_full_evidence_scores_at_or_near_the_ceiling():
    institution = _institution()
    branches = [
        Branch(branch_name=f"Campus {i}", city="Lahore", country_code="PK") for i in range(5)
    ]
    contacts = [
        ContactPoint(
            contact_type="phone", contact_value="+923001234567", person_name="Ayesha Malik"
        ),
        ContactPoint(contact_type="email", contact_value="admissions@riverside.edu"),
    ]
    qualification = QualificationAssessment(
        status=QualificationStatus.QUALIFIED, criteria_version=1
    )
    findings = [
        _finding("pain_points", ["slow admissions", "no CRM", "manual invoicing", "no website"]),
        _finding(
            "buying_signals",
            ["hiring an ops manager", "opened a new campus", "RFP", "demo request"],
        ),
    ]

    result = compute_lead_score(institution, branches, contacts, qualification, findings)

    assert result.overall_score == 100
    assert result.breakdown["scale"] == 15
    assert result.breakdown["contactability"] == 15
    assert result.breakdown["category_fit"] == 15
    assert result.breakdown["qualification"] == 20
    assert result.breakdown["research_signal"] == 20
    assert result.breakdown["freshness"] == 10
    assert result.breakdown["confidence"] == 5
    assert result.has_phone is True
    assert result.has_email is True
    assert result.has_named_contact is True
    assert result.evidence_count == 2


def test_single_source_confidence_score_does_not_score_max_confidence_points():
    # confidence_score is a 0-100 scale (canonical/merger.py:
    # confidence_for_source_count(1) == 10.0). Thresholding at >0.8/>0.5
    # (a 0-1 fraction assumption) meant ANY institution with even one
    # corroborating source (10.0 > 0.8) always hit the top confidence
    # tier -- this proves a single-source institution now correctly
    # scores the lowest tier instead.
    institution = _institution(confidence_score=10.0)

    result = compute_lead_score(institution, [], [], None, [])

    assert result.breakdown["confidence"] == 0


def test_disqualified_institution_gets_no_qualification_points():
    institution = _institution()
    qualification = QualificationAssessment(
        status=QualificationStatus.DISQUALIFIED, criteria_version=1
    )

    result = compute_lead_score(institution, [], [], qualification, [])

    assert result.breakdown["qualification"] == 0


def test_needs_review_qualification_gets_half_points():
    institution = _institution()
    qualification = QualificationAssessment(
        status=QualificationStatus.NEEDS_REVIEW, criteria_version=1
    )

    result = compute_lead_score(institution, [], [], qualification, [])

    assert result.breakdown["qualification"] == 10


def test_stale_findings_do_not_count_toward_freshness():
    institution = _institution()
    stale = _finding(
        "pain_points", ["old pain point"], created_at=datetime.now(UTC) - timedelta(days=90)
    )

    result = compute_lead_score(institution, [], [], None, [stale])

    assert result.breakdown["freshness"] == 0
    # The finding itself still counts as evidence, and still contributes to
    # research_signal -- freshness is a separate signal about recency, not a
    # gate on whether older evidence counts at all.
    assert result.evidence_count == 1
    assert result.breakdown["research_signal"] > 0


def test_only_the_latest_finding_per_key_counts_not_a_running_total():
    institution = _institution()
    older = _finding(
        "pain_points",
        ["a", "b", "c", "d"],
        created_at=datetime.now(UTC) - timedelta(days=5),
    )
    newer = _finding("pain_points", ["single pain point"], created_at=datetime.now(UTC))

    result = compute_lead_score(institution, [], [], None, [older, newer])

    # 1 pain point * 3 = 3 points, not 4 * 3 = 12 -- proves the older,
    # superseded finding's list length isn't the one used.
    assert result.breakdown["research_signal"] == 3
    assert result.evidence_count == 2


def test_score_never_exceeds_100_even_with_extra_contactability_stacking():
    institution = _institution()
    contacts = [
        ContactPoint(contact_type="phone", contact_value="+923001234567", person_name="A"),
        ContactPoint(contact_type="phone", contact_value="+923001234568", person_name="B"),
        ContactPoint(contact_type="email", contact_value="a@riverside.edu"),
        ContactPoint(contact_type="email", contact_value="b@riverside.edu"),
    ]
    branches = [
        Branch(branch_name=f"Campus {i}", city="Lahore", country_code="PK") for i in range(10)
    ]
    qualification = QualificationAssessment(
        status=QualificationStatus.QUALIFIED, criteria_version=1
    )
    findings = [
        _finding("pain_points", ["a", "b", "c", "d", "e"]),
        _finding("buying_signals", ["a", "b", "c", "d", "e"]),
    ]

    result = compute_lead_score(institution, branches, contacts, qualification, findings)

    assert result.overall_score == 100
