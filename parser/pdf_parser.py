import pdfplumber


def extract_text_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Fallback to PyMuPDF if pdfplumber found nothing
    if not text.strip():
        import fitz  # PyMuPDF
        with fitz.open(path) as doc:
            text = "\n".join(page.get_text() for page in doc)
    return text
