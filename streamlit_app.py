"""Recruitment Copilot - Streamlit frontend (3 logins + Milestone 1-3 screens).
Run:  streamlit run streamlit_app.py
"""
import os
import tempfile

import streamlit as st

st.set_page_config(page_title="Recruitment Copilot", page_icon="🧑‍💼", layout="wide")

CSS = """
<style>
html, body, [class*="css"] {font-family:'Inter',system-ui,sans-serif;}
.stApp {background:#f3f4f6;}
#MainMenu, footer, header {visibility:hidden;}
section[data-testid="stSidebar"] {background:#fff;border-right:1px solid #e5e7eb;}
.logo{display:flex;align-items:center;gap:10px;font-weight:600;margin:4px 0 18px;color:#111827}
.lg{width:34px;height:34px;border-radius:8px;background:linear-gradient(135deg,#2563eb,#dc2626);color:#fff;font-weight:700;font-size:12px;display:grid;place-items:center}
.card{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:16px;margin-bottom:14px;color:#111827}
.card h3{font-size:14px;font-weight:600;margin:0 0 12px}
.sub{color:#6b7280;font-size:13px}
.badge{background:#2563eb;color:#fff;padding:6px 12px;border-radius:6px;font-size:12px;font-weight:600;float:right}
.badge.g{background:#22c55e}.badge.o{background:#f59e0b}
.tag{display:inline-block;background:#dbeafe;color:#1d4ed8;border-radius:4px;padding:2px 8px;font-size:11px;margin:2px 3px 2px 0}
.stat{border:1px solid #e5e7eb;border-radius:8px;text-align:center;padding:8px;display:inline-block;width:31%;margin-right:1.5%;vertical-align:top}
.stat small{color:#6b7280;font-size:11px;display:block}.stat b{font-size:20px}
.bar{height:6px;background:#e5e7eb;border-radius:4px;overflow:hidden}.bar i{display:block;height:100%}
.kv{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;font-size:12px}.kv span{color:#6b7280}
.cand{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #e5e7eb}
.ring{width:46px;height:46px;border-radius:50%;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.ring small{font-size:8px;font-weight:500}
.sk{margin-bottom:14px;font-size:12px}.sk div.h{display:flex;justify-content:space-between;margin-bottom:5px}
.rec{background:#dbeafe;color:#1d4ed8;border-radius:8px;padding:12px;font-size:12px}
.q{display:flex;gap:10px;padding:10px 0;font-size:13px}.q i{background:#2563eb;color:#fff;border-radius:50%;min-width:20px;height:20px;font-size:11px;font-style:normal;display:grid;place-items:center}
.q small{color:#6b7280;display:block;margin-top:3px}
.chat{background:#f9fafb;border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:10px}
.m{max-width:85%;padding:10px 12px;border-radius:8px;font-size:12.5px;background:#fff;border:1px solid #e5e7eb}
.m.u{align-self:flex-end;background:#dbeafe;color:#1d4ed8;border-color:transparent}
.ats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
.ats div{border:1px solid #e5e7eb;border-radius:8px;padding:8px;font-size:12px}
.kp b{display:block;font-size:26px;margin:4px 0}.up{color:#22c55e;font-size:12px}
.pill{background:#dcfce7;color:#15803d;border-radius:4px;padding:2px 8px;font-size:11px}
.stButton>button{background:#2563eb;color:#fff;border:0;border-radius:6px;font-weight:600}
.stButton>button:hover{background:#1d4ed8;color:#fff}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

ROLES = {
    "candidate": dict(label="Candidate", title="Candidate sign in", desc="Upload your resume and attend AI screening.",
                      nav=["Dashboard", "Resume Upload", "Settings"]),
    "recruiter": dict(label="Recruiter", title="Recruiter sign in", desc="Rank candidates, review skill gaps and run interviews.",
                      nav=["Dashboard", "Resume Upload", "Candidates", "Settings"]),
    "admin": dict(label="Admin", title="Admin sign in", desc="View hiring analytics, approve candidates and manage reports.",
                  nav=["Dashboard", "Candidates", "Settings"]),
}
ICON = {"Dashboard": "▦", "Resume Upload": "📄", "Candidates": "👥", "Job Postings": "💼",
        "Analytics": "📊", "Interview Assistant": "💬", "Settings": "⚙"}

CANDS = {
    "Sarah Johnson": dict(m=92, tags=["Python", "TensorFlow", "ML", "NLP"],
        gaps=[("TensorFlow", "Advanced", "Required", 90, "#22c55e"), ("Kubernetes", "Intermediate", "Required", 55, "#f59e0b"),
              ("MLOps", "Basic", "Preferred", 30, "#ef4444"), ("AWS SageMaker", "None", "Required", 0, "#ef4444")],
        rec="Sarah shows strong ML fundamentals but needs development in deployment technologies. Consider AWS SageMaker certification and Kubernetes training to bridge gaps. Estimated learning time: 3-4 weeks."),
    "Michael Chen": dict(m=78, tags=["PyTorch", "Computer Vision", "Deep Learning"],
        gaps=[("TensorFlow", "Intermediate", "Required", 55, "#f59e0b"), ("Kubernetes", "Basic", "Required", 30, "#ef4444"),
              ("MLOps", "Intermediate", "Preferred", 55, "#f59e0b"), ("AWS SageMaker", "Basic", "Required", 25, "#ef4444")],
        rec="Michael has excellent deep learning depth. Focus on TensorFlow and Kubernetes for production work. Estimated learning time: 5-6 weeks."),
    "Emily Rodriguez": dict(m=85, tags=["R", "Statistics", "Data Viz"],
        gaps=[("TensorFlow", "Basic", "Required", 30, "#ef4444"), ("Kubernetes", "None", "Required", 0, "#ef4444"),
              ("MLOps", "Basic", "Preferred", 30, "#f59e0b"), ("AWS SageMaker", "Intermediate", "Required", 55, "#f59e0b")],
        rec="Emily has strong statistical foundations. Build engineering skills in TensorFlow and containerization. Estimated learning time: 6-8 weeks."),
}

S = st.session_state
S.setdefault("user", None)
S.setdefault("page", None)
S.setdefault("processed", 247)
S.setdefault("profiles", 235)
S.setdefault("parsed", dict(name="Sarah Johnson", email="sarah@example.com", phone="(555) 123-4567",
                            experience="5 years", education="MS Computer Science", location="San Francisco, CA",
                            skills=["Python", "Machine Learning", "Data Analysis", "TensorFlow", "SQL", "Project Management"],
                            file="Sarah_Johnson_Resume.pdf", size="1.2 MB"))
S.setdefault("recent", [("Sarah Johnson", "sarah@example.com", "5 years", ["Python", "ML", "SQL"]),
                        ("Michael Chen", "michael@example.com", "8 years", ["JavaScript", "React", "Node.js"])])
S.setdefault("chat", [("a", "Hello Sarah, I'm your AI interviewer today. Let's start with a technical question about your experience with machine learning deployment."),
                      ("u", "I'd be happy to discuss my experience with ML deployment."),
                      ("a", "Great! Can you describe your approach to monitoring machine learning models in production and how you handle model drift?")])


def tags(items):
    return "".join(f'<span class="tag">{t}</span>' for t in items)


S.setdefault("ukey", 0)
S.setdefault("last_file", None)
S.setdefault("last_parsed", None)
import json


def load_cands():
    try:
        with open("candidates.json", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []


def persist():
    try:
        with open("candidates.json", "w", encoding="utf-8") as fh:
            json.dump(S.cands, fh, ensure_ascii=False)
    except Exception:
        pass


S.setdefault("cands", load_cands())


def db_save(c):
    try:
        from database.db import SessionLocal
        from database.models import Candidate
        with SessionLocal() as db:
            db.add(Candidate(name=c["name"], email=c["email"], phone=c["phone"], skills=", ".join(c["skills"]),
                             education=", ".join(c["education"]), experience_years=c["experience"]))
            db.commit()
    except Exception:
        pass


def db_delete(email):
    try:
        from database.db import SessionLocal
        from database.models import Candidate
        with SessionLocal() as db:
            db.query(Candidate).filter(Candidate.email == email).delete()
            db.commit()
    except Exception:
        pass


def fields_found(c):
    good = lambda v: bool(v) and v not in ("-", "Not found")
    return sum([good(c["name"]), good(c["email"]), good(c["phone"]),
                c["experience"] > 0, bool(c["education"]), bool(c["skills"])])


def delete_candidate(i):
    c = S.cands.pop(i)
    persist()
    db_delete(c["email"])
    lp = S.last_parsed
    if lp and lp["email"] == c["email"] and lp["name"] == c["name"]:
        S.last_parsed = None
        S.last_file = None
        S.ukey += 1


def dashboard_block():
    cs = S.cands
    n = len(cs)
    pct = round(100 * sum(fields_found(c) for c in cs) / (6 * n)) if n else 0
    complete = sum(1 for c in cs if fields_found(c) == 6)
    uniq = len({sk.lower() for c in cs for sk in c["skills"]})
    cards = [("📄", "Resumes Processed", n), ("％", "Fields Found", f"{pct}%"),
             ("✔", "Complete Profiles", complete), ("✨", "Unique Skills Found", uniq)]
    ico = "width:44px;height:44px;border-radius:10px;background:#dbeafe;color:#2563eb;display:grid;place-items:center;font-size:18px"
    for col, (ic, lab, val) in zip(st.columns(4), cards):
        col.markdown(f'<div class="card" style="display:flex;gap:14px;align-items:center"><div style="{ico}">{ic}</div>'
                     f'<div><span class="sub">{lab}</span><br><b style="font-size:28px">{val}</b></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="margin-bottom:0"><h3 style="font-size:16px;margin:0">Recent Candidates</h3></div>', unsafe_allow_html=True)
    if not cs:
        st.info("No candidates yet. Upload a resume below.")
        return
    widths = [2, 3, 1.5, 2, 4, 1.5, 0.8]
    for col, t in zip(st.columns(widths), ["Candidate Name", "Email", "Experience", "Phone", "Key Skills", "Status", ""]):
        col.markdown(f'<span class="sub"><b>{t}</b></span>', unsafe_allow_html=True)
    for i, c in enumerate(list(cs)):
        c1, c2, c3, cp, c4, c5, c6 = st.columns(widths)
        c1.write(c["name"])
        c2.write(c["email"])
        cp.write(c.get("phone") or "-")
        c3.write(f'{c["experience"]} years' if c["experience"] else "-")
        extra = len(c["skills"]) - 3
        more = f'<span class="tag" style="background:#f3f4f6;color:#6b7280">+{extra}</span>' if extra > 0 else ""
        c4.markdown(tags(c["skills"][:3]) + more, unsafe_allow_html=True)
        c5.markdown('<span class="pill">Processed</span>', unsafe_allow_html=True)
        if c6.button("🗑", key=f"del_{i}_{c['email']}", help="Delete this candidate"):
            delete_candidate(i)
            st.rerun()


def head(title, sub, badge=None, cls=""):
    b = f'<span class="badge {cls}">{badge}</span>' if badge else ""
    st.markdown(f'{b}<h2 style="margin:0;font-size:22px;color:#111827">{title}</h2><p class="sub">{sub}</p>', unsafe_allow_html=True)


# ---------------------------------------------------------------- login pages
def login_page():
    role = st.query_params.get("login", "candidate")
    if role not in ROLES:
        role = "candidate"
    r = ROLES[role]
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown(f'<div class="card"><div class="logo"><div class="lg">RC</div>Recruitment Copilot</div>'
                    f'<h2 style="margin:0;font-size:22px">{r["title"]}</h2><p class="sub">{r["desc"]}</p></div>', unsafe_allow_html=True)
        email = st.text_input("Email", key=f"em_{role}", placeholder="you@company.com")
        pw = st.text_input("Password", key=f"pw_{role}", type="password")
        if st.button("Sign in", use_container_width=True, key=f"go_{role}"):
            if email and pw:
                S.user = dict(role=role, email=email)
                S.page = r["nav"][0]
                st.rerun()
            else:
                st.error("Enter your email and password to sign in.")
        st.caption("Demo: any email and password works.")
        cols = st.columns(2)
        for c, k in zip(cols, [k for k in ROLES if k != role]):
            if c.button(f"{ROLES[k]['label']} login", key=f"sw_{k}", use_container_width=True):
                st.query_params["login"] = k
                st.rerun()


# ---------------------------------------------------------------- pages
def page_dashboard():
    head("Dashboard", "Overview of your resume parsing activity", "Milestone 1")
    dashboard_block()


def page_upload():
    head("Resume Parsing & Candidate Profiling", "Overview, upload and process resumes to create structured candidate profiles", "Milestone 1")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown('<div class="card"><h3>📄 Upload Resume</h3><p class="sub">Supported formats: PDF, DOCX</p></div>', unsafe_allow_html=True)
        up = st.file_uploader("Drag and drop resumes or click to browse", type=["pdf", "docx"],
                              label_visibility="collapsed", key=f"up_{S.ukey}")
        if up is not None and S.last_file != (up.name, up.size):
            from parser.resume_parser import parse_resume
            suffix = os.path.splitext(up.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(up.getbuffer())
            ok = False
            try:
                c = parse_resume(tmp.name)
                cand = dict(name=c["name"] or "Not found", email=c["email"] or "-", phone=c["phone"] or "-",
                            experience=c["experience_years"], education=c["education"], skills=c["skills"])
                S.cands.insert(0, cand)
                S.last_parsed = dict(cand, file=up.name, size=f"{up.size / 1024:.0f} KB")
                S.last_file = (up.name, up.size)
                db_save(cand)
                persist()
                ok = True
            except Exception as e:
                st.error(f"Could not parse resume: {e}")
            finally:
                os.unlink(tmp.name)
            if ok:
                st.rerun()
        lp = S.last_parsed
        if lp:
            st.markdown(f'<div class="card" style="background:#dbeafe"><b>{lp["file"]}</b>'
                        f'<div class="sub" style="font-size:11px">Uploaded just now · {lp["size"]}</div></div>', unsafe_allow_html=True)
            if st.button("🗑 Remove this resume", key="rm_current"):
                for i, c in enumerate(S.cands):
                    if c["email"] == lp["email"] and c["name"] == lp["name"]:
                        delete_candidate(i)
                        break
                else:
                    S.last_parsed = None
                    S.last_file = None
                    S.ukey += 1
                st.rerun()
        else:
            st.caption("No resume uploaded yet.")
    with right:
        p = S.last_parsed or dict(name="-", email="-", phone="-", experience=0, education=[], skills=[])
        pct = round(100 * fields_found(p) / 6)
        exp = f'{p["experience"]} years' if p["experience"] else "-"
        st.markdown(f"""<div class="card"><h3>📊 Extracted Information</h3>
        <div style="display:flex;justify-content:space-between;font-size:12px"><span>Fields found</span><b style="color:#22c55e">{pct}%</b></div>
        <div class="bar"><i style="width:{pct}%;background:#22c55e"></i></div><br>
        <div class="kv"><div><span>Name:</span> {p["name"]}</div><div><span>Email:</span> {p["email"]}</div>
        <div><span>Phone:</span> {p["phone"]}</div><div><span>Experience:</span> {exp}</div>
        <div><span>Education:</span> {", ".join(p["education"]) or "-"}</div></div>
        <div style="margin-top:8px"><span class="sub">Skills:</span><br>{tags(p["skills"])}</div></div>""", unsafe_allow_html=True)


def page_candidates():
    head("Matching & Skill Analysis", "Candidate-job matching and skill-gap analysis", "Milestone 2", "g")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="card"><h3>👥 Candidate Matching</h3></div>', unsafe_allow_html=True)
        st.selectbox("Job Position", ["Senior Machine Learning Engineer", "Data Scientist"])
        for n, d in CANDS.items():
            color = "#22c55e" if d["m"] >= 90 else "#f59e0b"
            st.markdown(f'<div class="card cand"><div><b>{n}</b><br>{tags(d["tags"])}</div><div class="ring" style="background:{color}">{d["m"]}%<small>Match</small></div></div>', unsafe_allow_html=True)
    with right:
        who = st.selectbox("Candidate", list(CANDS), key="gap_who")
        d = CANDS[who]
        bars = "".join(
            f'<div class="sk"><div class="h"><b>{s}</b><span>{lvl} <span style="color:{"#ef4444" if req=="Required" else "#f59e0b"}">{req}</span></span></div>'
            f'<div class="bar"><i style="width:{pct}%;background:{c}"></i></div></div>' for s, lvl, req, pct, c in d["gaps"])
        st.markdown(f'<div class="card"><h3>📈 Skill Gap Analysis</h3>{bars}<div class="rec"><b>Recommendations</b><br>{d["rec"]}</div></div>', unsafe_allow_html=True)


def page_interview():
    head("Interview Assistance & ATS Integration", "Generate interview questions, simulate interviews, and manage candidates", "Milestone 3", "o")
    left, right = st.columns(2)
    qs = [("Describe a machine learning project where you had to optimize model performance. What techniques did you use and what was the outcome?", "Technical • Experience-based • 3-5 min response"),
          ("How would you approach deploying a machine learning model in a production environment? What considerations would you take into account?", "Technical • Scenario-based • 4-6 min response"),
          ("Tell me about a time when you had to explain complex technical concepts to non-technical stakeholders. How did you ensure they understood?", "Behavioral • Communication • 2-4 min response")]
    with left:
        a, b = st.columns(2)
        a.selectbox("Job Position", ["Senior ML Engineer"])
        b.selectbox("Question Type", ["Technical Skills", "Behavioral"])
        items = "".join(f'<div class="q"><i>{i+1}</i><div>{q}<small>{m}</small></div></div>' for i, (q, m) in enumerate(qs))
        st.markdown(f'<div class="card"><h3>📋 Interview Question Generator</h3>{items}</div>', unsafe_allow_html=True)
    with right:
        msgs = "".join(f'<div class="m {k}">{t}</div>' for k, t in S.chat)
        st.markdown(f'<div class="card"><h3>🎙 AI Interview Simulation</h3><p class="sub">Candidate: Sarah Johnson <span style="color:#22c55e;float:right">● Active Session</span></p><div class="chat">{msgs}</div></div>', unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            txt = st.text_input("Type your response...", label_visibility="collapsed", placeholder="Type your response...")
            if st.form_submit_button("Send") and txt.strip():
                S.chat += [("u", txt.strip()), ("a", "Thanks. Can you give a specific example, including the metrics you used to measure success?")]
                st.rerun()
        st.markdown('<div class="card"><b>ATS Integration</b> <span style="color:#22c55e;float:right;font-size:12px">● Connected</span>'
                    '<div class="ats"><div><b>Sarah Johnson</b><br>Interview in progress</div><div><b>Michael Chen</b><br>Scheduled for tomorrow</div></div></div>', unsafe_allow_html=True)


def page_jobs():
    head("Job Postings", "Manage open roles and upload job descriptions")
    st.table({"Role": ["Senior ML Engineer", "Senior Data Scientist", "Data Analyst"],
              "Required skills": ["Python, TensorFlow, Kubernetes", "Python, SQL, TensorFlow", "SQL, Power BI, Tableau"],
              "Experience": ["5+ years", "3+ years", "2+ years"], "Applicants": [86, 64, 47]})


def page_analytics():
    head("Analytics", "Hiring analytics and reports")
    st.bar_chart({"Resumes processed": [120, 160, 110, 190, 140]})


def page_settings():
    head("Settings", "Account and notification preferences")
    st.write(f"Role: **{ROLES[S.user['role']]['label']}**  \nEmail: **{S.user['email']}**")


PAGES = {"Dashboard": page_dashboard, "Resume Upload": page_upload, "Candidates": page_candidates, "Job Postings": page_jobs,
         "Analytics": page_analytics, "Interview Assistant": page_interview, "Settings": page_settings}

# ---------------------------------------------------------------- router
if not S.user:
    login_page()
else:
    role = ROLES[S.user["role"]]
    with st.sidebar:
        st.markdown('<div class="logo"><div class="lg">RC</div>Recruitment Copilot</div>', unsafe_allow_html=True)
        for p in role["nav"]:
            if st.button(f"{ICON[p]}  {p}", key=f"nav_{p}", use_container_width=True, type="primary" if S.page == p else "secondary"):
                S.page = p
                st.rerun()
        nm = S.user["email"].split("@")[0].title()
        st.markdown(f'<div style="display:flex;gap:10px;align-items:center;border-top:1px solid #e5e7eb;padding-top:12px;margin-top:12px"><div style="width:34px;height:34px;border-radius:50%;background:#dbeafe;color:#2563eb;font-weight:600;display:grid;place-items:center">{nm[:1]}</div><div><b>{nm}</b><br><span class="sub">{role["label"]}</span></div></div>', unsafe_allow_html=True)
        if st.button("Sign out"):
            S.user = None
            st.rerun()
    PAGES[S.page if S.page in role["nav"] else role["nav"][0]]()
