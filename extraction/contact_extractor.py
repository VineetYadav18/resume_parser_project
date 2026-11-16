import re

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            _nlp = False
    return _nlp


EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_PATTERN = r"(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|[6-9]\d{4}[-.\s]?\d{5})"


def extract_email(text):
    emails = re.findall(EMAIL_PATTERN, text)
    return emails[0] if emails else ""


def extract_phone(text):
    match = re.search(PHONE_PATTERN, text)
    return match.group(0).strip() if match else ""


def extract_name(text):
    # 1) Heuristic: name is usually one of the first non-empty lines
    for line in [l.strip() for l in text.splitlines() if l.strip()][:5]:
        if "@" in line or re.search(r"\d", line):
            continue
        words = line.split()
        if 2 <= len(words) <= 4 and all(re.fullmatch(r"[A-Za-z.'-]+", w) for w in words):
            if line.lower() not in {"curriculum vitae", "professional summary"}:
                return line.title() if line.isupper() else line

    # 2) spaCy NER on the top of the document
    nlp = _get_nlp()
    if nlp:
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
    return ""
