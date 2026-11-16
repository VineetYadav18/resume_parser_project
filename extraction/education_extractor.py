import re

DEGREES = {
    "B.Tech": r"b\.?\s?tech", "M.Tech": r"m\.?\s?tech", "MBA": r"mba", "BCA": r"bca",
    "MCA": r"mca", "B.Sc": r"b\.?\s?sc", "M.Sc": r"m\.?\s?sc", "PhD": r"ph\.?\s?d",
    "Bachelor": r"bachelor(?:'s)?", "Master": r"master(?:'s)?",
}
_PATTERNS = {k: re.compile(r"(?<![A-Za-z0-9])" + v + r"(?![A-Za-z0-9])", re.I) for k, v in DEGREES.items()}


def extract_education(text):
    results = [name for name, pat in _PATTERNS.items() if pat.search(text)]
    # "B.E" is case-sensitive so the word "be" never matches
    if re.search(r"\bB\.\s?E\b\.?|\bBE\b", text):
        results.insert(0, "B.E")
    return results
