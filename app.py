import json
from pathlib import Path

import streamlit as st
import pandas as pd

from ncalas.document import extract_text
from ncalas.prototype import (
    verify_review_cues, localize_matches, draft_defense_questions,
    lexical_response_signal
)
from ncalas.storage import log_event


st.set_page_config(page_title="N-CALAS | VLD Prototype", page_icon="🧭", layout="wide")
st.title("N-CALAS")
st.caption("Nigerian Critical AI Literacy Assessment System · Verify – Localize – Defend")

st.warning(
    "Prototype only. This demonstrator does not fact-check claims, interpret standards, "
    "measure AI authorship or assign validated student scores. All outputs require "
    "qualified human review. Use synthetic or non-identifiable material."
)

profile_path = Path("config/institution.json")
example_path = Path("config/institution.example.json")
profile = {}
try:
    profile = json.loads((profile_path if profile_path.exists() else example_path).read_text(encoding="utf-8"))
except Exception as exc:
    st.error(f"Could not load institution profile: {exc}")

with st.sidebar:
    st.header("Institution profile")
    st.write(profile.get("institution", {}).get("name", "Not configured"))
    st.caption("Edit config/institution.json locally to configure this demonstrator.")
    st.divider()
    st.write("Profile version:", profile.get("institution", {}).get("profile_version", "unknown"))

uploaded = st.file_uploader("Upload a report", type=["txt", "md", "pdf", "docx"])
pasted = st.text_area("Or paste report text", height=180, placeholder="Paste a short report excerpt...")
report_text = pasted.strip()
if uploaded is not None:
    try:
        report_text = extract_text(uploaded.name, uploaded.getvalue()).strip()
        st.caption(f"Extracted text from {uploaded.name}")
    except Exception as exc:
        st.error(f"Document extraction failed: {exc}")

if st.button("Review report", type="primary", disabled=not bool(report_text)):
    st.session_state["ncalas_report"] = report_text
    st.session_state["ncalas_verify"] = verify_review_cues(report_text)
    st.session_state["ncalas_localize"] = localize_matches(report_text, profile)
    st.session_state["ncalas_questions"] = draft_defense_questions(report_text)
    log_event("prototype_review_run", "Text processed locally; report content not written to activity log.")
    st.success("Review cues generated. These are not assessment scores.")

if "ncalas_report" in st.session_state:
    vtab, ltab, dtab = st.tabs(["1 · Verify", "2 · Localize", "3 · Defend"])

    with vtab:
        st.subheader("Verify: items requiring evidence checks")
        st.caption("The prototype surfaces candidates only. An examiner must verify each claim against suitable evidence.")
        cues = st.session_state.get("ncalas_verify", [])
        if cues:
            st.dataframe(pd.DataFrame(cues), use_container_width=True, hide_index=True)
        else:
            st.info("No review cues were detected by the current simple patterns. This does not mean the report is accurate.")

    with ltab:
        st.subheader("Localize: configured term checks")
        st.caption("Literal matching only. Absence or presence of a term does not establish compliance.")
        matches = st.session_state.get("ncalas_localize", [])
        if matches:
            st.dataframe(pd.DataFrame(matches), use_container_width=True, hide_index=True)
        else:
            st.info("No localization terms are configured. Add institution-approved terms to the profile.")

    with dtab:
        st.subheader("Defend: draft report-grounded questions")
        st.caption("Review, edit and select questions before any student interaction.")
        questions = st.session_state.get("ncalas_questions", [])
        for i, question in enumerate(questions, 1):
            st.markdown(f"**Q{i}.** {question}")
        selected = st.selectbox("Choose a question for a response demonstration", questions)
        answer = st.text_area("Demonstration response", key="defense_answer")
        if st.button("Inspect response wording", disabled=not answer.strip()):
            signal = lexical_response_signal(selected, answer)
            st.json(signal)
            st.info("This descriptive signal is not a judgment of understanding, correctness or authorship.")

st.divider()
st.caption("N-CALAS early demonstrator · Keep Verify, Localize and Defend evidence separate · Human examiner review required.")
