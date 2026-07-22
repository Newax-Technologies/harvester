from __future__ import annotations

import datetime
import uuid

from .config import Settings
from .entities.institution import Institution
from .entities.branch import Branch
from .entities.contact import ContactPoint
from .entities.signal import OpportunitySignal
from .storage.sqlite import SQLiteStore
from .sources.google_places import GooglePlacesConnector
from .sources.geographic_tiling import generate_tiles, build_queries_for_tile
from .intelligence.taxonomy import identify_institution_type
from .intelligence.scoring import score_opportunity
from .intelligence.pain_detection import detect_pain_points, generate_reason_to_contact
from .resolution.deduplication import Deduplicator
from .enrichment.website_analyzer import analyze_website

class LeadPipeline:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.store = SQLiteStore(settings.database_path)
        self.places_connector = GooglePlacesConnector(api_key=settings.google_places_api_key)

    def run(self):
        tiles = generate_tiles(self.settings.job_config)
        categories = self.settings.job_config.get("categories", ["FORMAL_EDUCATION"])
        
        # Load existing institutions for deduplication
        existing_institutions = [] # In a real app we'd load this from self.store
        deduplicator = Deduplicator(existing_institutions)
        
        for tile in tiles:
            queries = build_queries_for_tile(tile, categories)
            for query in queries:
                print(f"Executing Google Places query: {query}")
                places = self.places_connector.search(query)
                
                for place in places:
                    self.process_place(place, deduplicator)

    def process_place(self, place: dict, deduplicator: Deduplicator):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        domain = ""
        website_url = place.get("websiteUri", "")
        if website_url:
            domain = website_url.replace("https://", "").replace("http://", "").split("/")[0]

        inst = Institution(
            id=place.get("id", str(uuid.uuid4())),
            canonical_name=place.get("displayName", {}).get("text", "Unknown"),
            institution_type=identify_institution_type(place.get("displayName", {}).get("text", "Unknown"), ""),
            website=website_url,
            domain=domain,
            primary_phone=place.get("nationalPhoneNumber", ""),
            discovered_at=now,
            raw_data=place
        )

        match = deduplicator.find_match(inst)
        if match:
            inst = match
        else:
            deduplicator.institutions.append(inst)
            
        branch = Branch(
            id=str(uuid.uuid4()),
            institution_id=inst.id,
            address=place.get("formattedAddress", ""),
            map_provider_ids={"google_places": place.get("id", "")}
        )
        
        contact = None
        if inst.primary_phone:
            contact = ContactPoint(
                id=str(uuid.uuid4()),
                institution_id=inst.id,
                phone=inst.primary_phone,
                source="Google Places",
                publicly_listed=True
            )
            
        signals = []
        if website_url:
            raw_website_data = analyze_website(website_url)
            signals = detect_pain_points(inst, raw_website_data)
            
        reason = generate_reason_to_contact(inst, [branch], signals)
        
        # Score
        score = score_opportunity(inst, [branch], [contact] if contact else [], signals)
        inst.confidence = score / 100.0 # Just storing score as confidence for now
        
        self.store.upsert_institution(inst)
        self.store.upsert_branch(branch)
        if contact:
            self.store.upsert_contact_point(contact)
        for sig in signals:
            self.store.upsert_opportunity_signal(sig)
