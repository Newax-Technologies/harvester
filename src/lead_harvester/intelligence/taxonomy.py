FORMAL_EDUCATION = [
    "school", "private school", "college", "montessori", "preschool", 
    "daycare", "early learning center", "special education", "boarding school"
]

ACADEMIC_SUPPORT = [
    "tuition center", "coaching academy", "o level academy", "a level academy",
    "matric academy", "fsc academy", "home tuition", "online academy", 
    "language institute", "stem academy", "coding academy"
]

EXAM_PREPARATION = [
    "mdcat academy", "ecat academy", "css academy", "ielts institute",
    "pte institute", "sat center", "gre center", "test preparation"
]

RELIGIOUS_EDUCATION = [
    "madrasa", "quran academy", "hifz institute", "islamic school", "weekend islamic school"
]

EXTRACURRICULAR = [
    "football academy", "cricket academy", "martial arts school", "swimming academy",
    "gymnastics center", "music school", "art academy", "public speaking center",
    "robotics center"
]

ALL_CATEGORIES = {
    "FORMAL_EDUCATION": FORMAL_EDUCATION,
    "ACADEMIC_SUPPORT": ACADEMIC_SUPPORT,
    "EXAM_PREPARATION": EXAM_PREPARATION,
    "RELIGIOUS_EDUCATION": RELIGIOUS_EDUCATION,
    "EXTRACURRICULAR": EXTRACURRICULAR
}

def get_synonyms(category_key: str) -> list[str]:
    return ALL_CATEGORIES.get(category_key, [])

def identify_institution_type(name: str, description: str) -> str:
    haystack = f"{name} {description}".lower()
    for category, terms in ALL_CATEGORIES.items():
        if any(term in haystack for term in terms):
            return category
    return "UNKNOWN"
