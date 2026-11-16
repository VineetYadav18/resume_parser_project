import csv
import os
import re
from difflib import get_close_matches

_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills", "skills.csv")

with open(_PATH, newline="", encoding="utf-8") as f:
    SKILLS = [row[0].strip() for row in csv.reader(f) if row and row[0].strip()]

ALIASES = {
    "sklearn": "Scikit-Learn", "scikit learn": "Scikit-Learn", "node.js": "NodeJS",
    "nodejs": "NodeJS", "ml": "Machine Learning", "tf": "TensorFlow", "powerbi": "Power BI",
    "postgres": "PostgreSQL", "k8s": "Kubernetes", "google cloud": "GCP", "ai": "Artificial Intelligence",
}


def _pattern(term):
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term.lower()) + r"(?![A-Za-z0-9])")


_PATTERNS = {s: _pattern(s) for s in SKILLS}
_ALIAS_PATTERNS = {a: (_pattern(a), s) for a, s in ALIASES.items()}


def extract_skills(text):
    low = text.lower()
    found = set()

    for skill, pat in _PATTERNS.items():
        if pat.search(low):
            found.add(skill)
    for _, (pat, skill) in _ALIAS_PATTERNS.items():
        if pat.search(low):
            found.add(skill)

    # Fuzzy matching for typos (single-word skills only)
    lowered = {s.lower(): s for s in SKILLS if " " not in s and len(s) > 4}
    for token in set(re.findall(r"[a-z][a-z+#.-]{4,}", low)):
        if token in lowered:
            continue
        match = get_close_matches(token, list(lowered), n=1, cutoff=0.9)
        if match:
            found.add(lowered[match[0]])

    return sorted(found)
