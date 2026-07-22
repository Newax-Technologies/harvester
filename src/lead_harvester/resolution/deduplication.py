import math
from ..entities.institution import Institution
from .normalization import normalize_institution_name, normalize_url, normalize_phone

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Earth radius in meters
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_similarity(name1: str, name2: str) -> float:
    # Basic Jaccard similarity for now
    n1 = normalize_institution_name(name1).split()
    n2 = normalize_institution_name(name2).split()
    if not n1 or not n2:
        return 0.0
    set1 = set(n1)
    set2 = set(n2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

class Deduplicator:
    def __init__(self, existing_institutions: list[Institution]):
        self.institutions = existing_institutions

    def find_match(self, target: Institution) -> Institution | None:
        target_domain = normalize_url(target.domain) if target.domain else None
        target_phone = normalize_phone(target.primary_phone) if target.primary_phone else None
        
        best_match = None
        best_score = 0.0

        for inst in self.institutions:
            # Exact Match Layer
            if target_domain and inst.domain and target_domain == normalize_url(inst.domain):
                return inst
            if target_phone and inst.primary_phone and target_phone == normalize_phone(inst.primary_phone):
                return inst
            
            # Fuzzy Match Layer
            similarity = calculate_similarity(target.canonical_name, inst.canonical_name)
            # Distance would require branches to check properly, but this is a stub for the logic
            # If we had lat/lon on institution, we could do distance checks here
            
            if similarity > 0.85 and similarity > best_score:
                best_score = similarity
                best_match = inst

        if best_score > 0.90:
            return best_match

        return None
