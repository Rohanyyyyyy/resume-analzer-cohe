import streamlit as st
import fitz  # PyMuPDF
from analyzer import get_match_score, get_keyword_suggestions

st.set_page_config(page_title="Resume vs Job Description Analyzer", layout="centered")
st.title("📄 Resume & JD Analyzer (Cohere AI)")

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

def extract_text(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

if resume_file and jd_file:
    resume_text = extract_text(resume_file)
    jd_text = extract_text(jd_file)

    st.subheader("Resume Preview")
    st.text_area("Resume Text", resume_text, height=200)

    st.subheader("Job Description Preview")
    st.text_area("Job Description Text", jd_text, height=200)

    match_score = get_match_score(resume_text, jd_text)
    st.subheader("Match Score")
    st.progress(match_score / 100)
    st.write(f"📊 **{match_score:.2f}%** resume-job match")

    suggestions = get_keyword_suggestions(resume_text, jd_text)
    st.subheader("🧠 AI Keyword Suggestions")
    st.write(suggestions)
