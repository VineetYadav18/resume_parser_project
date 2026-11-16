import re

PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", re.I)


def extract_experience(text):
    values = [float(m) for m in PATTERN.findall(text)]
    values = [v for v in values if v <= 45]  # ignore e.g. "100 years of company history"
    return int(max(values)) if values else 0
