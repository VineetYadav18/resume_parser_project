# Resume Parser (Milestone 1)
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    psql -U postgres -f schema.sql
    uvicorn app:app --reload
Swagger: http://localhost:8000/docs
Override the DB with: DATABASE_URL=postgresql://user:pass@host/hiringdb
