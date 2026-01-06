# src/skills_normalizer.py

from typing import List, Dict, Set
import re

# -------------------------------------------------------------------
# Canonical Skill Ontology
# -------------------------------------------------------------------
# This is intentionally small at first.
# It will grow over time and can be versioned.
CANONICAL_SKILLS: Dict[str, Set[str]] = {
    "machine learning": {
        "ml", "machine learning", "ml algorithms", "supervised learning",
        "unsupervised learning"
    },
    "deep learning": {
        "deep learning", "dl", "neural networks", "cnn", "rnn"
    },
    "natural language processing": {
        "nlp", "natural language processing", "text mining", "language models"
    },
    "computer vision": {
        "computer vision", "cv", "image processing", "object detection"
    },
    "python": {
        "python", "python programming"
    },
    "sql": {
        "sql", "mysql", "postgresql", "sqlite"
    },
    "pandas": {"pandas"},
    "numpy": {"numpy"},
    "scikit-learn": {"scikit-learn", "sklearn"},
    "tensorflow": {"tensorflow", "tf"},
    "pytorch": {"pytorch", "torch"},
    "data analysis": {"data analysis", "data analytics"},
    "statistics": {"statistics", "statistical analysis"},
}

# Reverse lookup table: alias → canonical
_ALIAS_TO_CANONICAL = {
    alias: canonical
    for canonical, aliases in CANONICAL_SKILLS.items()
    for alias in aliases
}

# -------------------------------------------------------------------
# Core Normalization Functions
# -------------------------------------------------------------------

def _basic_clean(skill: str) -> str:
    """
    Perform minimal, deterministic cleaning.
    Avoid aggressive NLP to preserve traceability.
    """
    skill = skill.lower()
    skill = re.sub(r"[^a-z0-9\s\+\-\.]", "", skill)
    skill = re.sub(r"\s+", " ", skill).strip()
    return skill


def normalize_skill(skill: str) -> str:
    """
    Normalize a single skill to its canonical form if known.
    Otherwise, return the cleaned skill.
    """
    cleaned = _basic_clean(skill)
    return _ALIAS_TO_CANONICAL.get(cleaned, cleaned)


def normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalize a list of skills.
    - cleans
    - maps to canonical forms
    - removes duplicates
    """
    normalized = {normalize_skill(s) for s in skills if s and s.strip()}
    return sorted(normalized)
