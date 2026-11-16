import os

from parser.pdf_parser import extract_text_pdf
from parser.docx_parser import extract_text_docx
from extraction.contact_extractor import extract_name, extract_email, extract_phone
from extraction.skill_extractor import extract_skills
from extraction.education_extractor import extract_education
from extraction.experience_extractor import extract_experience


def parse_resume(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = extract_text_pdf(path)
    elif ext == ".docx":
        text = extract_text_docx(path)
    else:
        raise ValueError("Unsupported file type. Upload a PDF or DOCX resume.")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience(text),
        "resume_text": text,
    }
