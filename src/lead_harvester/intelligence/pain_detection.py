from typing import Any
from ..entities.institution import Institution
from ..entities.signal import OpportunitySignal

def detect_pain_points(institution: Institution, raw_website_data: str) -> list[OpportunitySignal]:
    signals = []
    
    # Very basic text detection for phase 1
    # Check for whatsapp communication
    if "whatsapp" in raw_website_data.lower() and "parent portal" not in raw_website_data.lower():
        signals.append(OpportunitySignal(
            id=f"{institution.id}_pain_1",
            institution_id=institution.id,
            signal_type="PAIN",
            signal_text="Uses WhatsApp for communication, lacks parent portal.",
            confidence=0.8,
            commercial_relevance=0.8
        ))
        
    # Check for admissions
    if "google form" in raw_website_data.lower() and "admission" in raw_website_data.lower():
        signals.append(OpportunitySignal(
            id=f"{institution.id}_pain_2",
            institution_id=institution.id,
            signal_type="PAIN",
            signal_text="Uses Google Forms for admissions.",
            confidence=0.9,
            commercial_relevance=0.9
        ))
        
    return signals

def classify_opportunity(institution: Institution, branches: list[Any], signals: list[OpportunitySignal]) -> str:
    pain_signals = [s for s in signals if s.signal_type == "PAIN"]
    
    if not institution.website:
        return "Type A: Digitally absent"
    elif len(branches) >= 2 and len(pain_signals) == 0:
        return "Type C: Growing institution"
    else:
        return "Type B: Digitally fragmented"

def generate_reason_to_contact(institution: Institution, branches: list[Any], signals: list[OpportunitySignal]) -> str:
    opp_type = classify_opportunity(institution, branches, signals)
    pain_points = ", ".join([s.signal_text for s in signals if s.signal_type == "PAIN"])
    
    return f"Opportunity: {opp_type}. Detected Pains: {pain_points or 'None detected'}. Recommended Pitch: Offer CRM and Automation."
