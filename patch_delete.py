import re
f = "streamlit_app.py"
s = open(f, encoding="utf-8").read()

HELPERS = '''def db_delete(email):
    try:
        from database.db import SessionLocal
        from database.models import Candidate
        with SessionLocal() as db:
            db.query(Candidate).filter(Candidate.email == email).delete()
            db.commit()
    except Exception:
        pass


def remove_current():
    p = S.parsed
    db_delete(p["email"])
    S.recent = [r for r in S.recent if r[1] != p["email"]]
    S.processed = max(0, S.processed - 1)
    S.profiles = max(0, S.profiles - 1)
    S.parsed = dict(name="-", email="-", phone="-", experience="-", education="-", location="-",
                    skills=[], file="No resume uploaded", size="0 KB")
    S.last_file = None
    S.ukey = S.get("ukey", 0) + 1


def head('''
a = 'def head('
assert s.count(a) == 1
s = s.replace(a, HELPERS)

a = 'type=["pdf", "docx"], label_visibility="collapsed")'
assert s.count(a) == 1
s = s.replace(a, 'type=["pdf", "docx"], label_visibility="collapsed", key=f"up_{S.get(\'ukey\', 0)}")')

a = '    with right:\n        p = S.parsed\n'
assert s.count(a) == 1
s = s.replace(a, '        if st.button("🗑 Remove this resume", key="rm_current"):\n            remove_current()\n            st.rerun()\n' + a)

NEW = '''    st.markdown('<div class="card"><h3>👥 Recently Processed Candidates</h3></div>', unsafe_allow_html=True)
    for i, (n, e, x, k) in enumerate(list(S.recent)):
        c1, c2, c3, c4, c5 = st.columns([2, 3, 1.5, 3, 1])
        c1.write(n)
        c2.write(e)
        c3.write(x)
        c4.markdown(tags(k), unsafe_allow_html=True)
        if c5.button("🗑", key=f"del_{i}_{e}", help="Delete this candidate"):
            db_delete(e)
            S.recent.pop(i)
            S.processed = max(0, S.processed - 1)
            S.profiles = max(0, S.profiles - 1)
            st.rerun()
'''
pat = re.compile(r'    rows = "".join\(.*?</table></div>\', unsafe_allow_html=True\)\n', re.S)
assert len(pat.findall(s)) == 1
s = pat.sub(lambda m: NEW, s)
open(f, "w", encoding="utf-8").write(s)
print("Patched OK")
