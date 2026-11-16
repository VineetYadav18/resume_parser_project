import os
import shutil
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from parser.resume_parser import parse_resume
from database.db import engine, SessionLocal
from database.models import Base, Candidate

app = FastAPI(title="Recruitment Copilot - Resume Parser")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

try:
    Base.metadata.create_all(engine)
except Exception as e:  # DB not running yet: parsing still works
    print("Database unavailable:", e)


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".docx"):
        raise HTTPException(400, "Only PDF and DOCX resumes are supported.")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        candidate = parse_resume(file_path)
    except Exception as e:
        raise HTTPException(422, f"Could not parse resume: {e}")

    saved = False
    try:
        with SessionLocal() as db:
            row = Candidate(
                name=candidate["name"], email=candidate["email"], phone=candidate["phone"],
                skills=", ".join(candidate["skills"]), education=", ".join(candidate["education"]),
                experience_years=candidate["experience_years"],
            )
            db.add(row)
            db.commit()
            candidate["id"] = row.id
            saved = True
    except Exception as e:
        print("DB save failed:", e)

    candidate["saved_to_db"] = saved
    return candidate


@app.get("/candidates")
def list_candidates():
    with SessionLocal() as db:
        rows = db.query(Candidate).order_by(Candidate.id.desc()).all()
        return [
            {"id": r.id, "name": r.name, "email": r.email, "phone": r.phone,
             "skills": (r.skills or "").split(", "), "education": (r.education or "").split(", "),
             "experience_years": r.experience_years}
            for r in rows
        ]
