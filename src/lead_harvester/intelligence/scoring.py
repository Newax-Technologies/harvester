from ..entities.branch import Branch
from ..entities.contact import ContactPoint
from ..entities.institution import Institution
from ..entities.signal import OpportunitySignal


def score_opportunity(
    institution: Institution,
    branches: list[Branch],
    contacts: list[ContactPoint],
    signals: list[OpportunitySignal],
) -> int:
    score = 0

    # 1. Estimated Institution Scale (Max 15)
    branch_count = len(branches)
    if branch_count >= 5:
        score += 15
    elif branch_count >= 3:
        score += 10
    elif branch_count >= 2:
        score += 5

    # 2. Operational Pain (Max 25)
    pain_score = 0
    for signal in signals:
        if signal.signal_type == "PAIN":
            pain_score += min(10, int(signal.commercial_relevance * 10))
    score += min(25, pain_score)

    # 3. Current Buying/Expansion Signals (Max 20)
    buying_score = 0
    for signal in signals:
        if signal.signal_type in ["GROWTH", "PROCUREMENT", "HIRING"]:
            buying_score += min(10, int(signal.commercial_relevance * 10))
    score += min(20, buying_score)

    # 4. Contactability (Max 10)
    has_phone = any(c.phone for c in contacts) or institution.primary_phone
    has_email = any(c.email for c in contacts) or institution.primary_email
    has_website = bool(institution.website)

    if has_phone and has_website:
        score += 8
    elif has_phone:
        score += 5
    if has_email:
        score += 2

    # 5. ICP/Category Fit (Max 15)
    if institution.institution_type != "UNKNOWN":
        score += 15

    # 6. Recency (Max 5)
    recent_signals = [s for s in signals if s.freshness <= 30]  # 30 days
    if recent_signals:
        score += 5

    # 7. Data Confidence (Max 5)
    if institution.confidence > 0.8:
        score += 5
    elif institution.confidence > 0.5:
        score += 2

    return min(100, score)
