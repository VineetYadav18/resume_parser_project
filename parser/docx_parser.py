from docx import Document


def extract_text_docx(path):
    document = Document(path)
    lines = [para.text for para in document.paragraphs]

    # Many resumes use tables for layout
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                lines.extend(p.text for p in cell.paragraphs)

    return "\n".join(l for l in lines if l.strip())
