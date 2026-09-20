"""
Intelligent Document Extraction & Analysis System
Streamlit UI + Groq LLM backend — advanced edition.

Advanced features:
  - Batch multi-document upload & processing
  - Confidence / self-validation pass on extracted fields
  - Analytics dashboard (completeness, confidence breakdown)
  - Cross-document comparison
  - Keyword search & highlight in raw text
  - Extraction history panel
  - Excel export (in addition to JSON/CSV)
"""

import io
import re
import json
from datetime import datetime

import streamlit as st
import pandas as pd

from utils.extractor import extract_text_from_file
from utils.groq_client import (
    extract_structured_data,
    validate_extraction,
    summarize_document,
    ask_document_question,
    compare_documents,
)
from utils.schema import SCHEMA_TEMPLATES
from utils.styling import inject_custom_css

st.set_page_config(page_title="Doc Extraction & Analysis", page_icon="📄", layout="wide")
inject_custom_css(st)

# ---------- Session State ----------
if "documents" not in st.session_state:
    # keyed by filename -> {text, structured_data, confidence, summary, schema, processed_at}
    st.session_state.documents = {}
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts, newest first
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}  # keyed by filename -> list of messages

# ---------- Sidebar ----------
st.sidebar.title("⚙️ Configuration")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", value="")
model_choice = st.sidebar.selectbox(
    "Model",
    ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"],
)
st.sidebar.caption("Model list current as of Groq's Aug 2026 deprecations — check console.groq.com/docs/models if a call 404s.")

doc_type = st.sidebar.selectbox("Document Type", list(SCHEMA_TEMPLATES.keys()))
st.sidebar.subheader("Extraction Schema (JSON)")
schema_text = st.sidebar.text_area(
    "Fields to extract",
    value=json.dumps(SCHEMA_TEMPLATES[doc_type], indent=2),
    height=200,
)
run_validation = st.sidebar.checkbox("🔍 Run confidence validation pass", value=True,
                                      help="Extra LLM call that fact-checks each extracted field against the source text.")

st.sidebar.divider()
st.sidebar.subheader("🕘 History")
if st.session_state.history:
    for h in st.session_state.history[:8]:
        st.sidebar.caption(f"{h['time']} — {h['filename']} ({h['model']})")
else:
    st.sidebar.caption("No extractions yet this session.")

# ---------- Helpers ----------
def confidence_badge_html(level: str) -> str:
    level = (level or "medium").lower()
    cls = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}.get(level, "badge-medium")
    return f'<span class="badge {cls}">{level.upper()}</span>'


def highlight_text(text: str, query: str) -> str:
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f'<mark class="hl">{m.group(0)}</mark>', text)


def to_excel_bytes(data: dict) -> bytes:
    buffer = io.BytesIO()
    df = pd.json_normalize(data)
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Extracted Data")
    return buffer.getvalue()


def field_completeness(data: dict) -> float:
    if not data:
        return 0.0
    filled = sum(1 for v in data.values() if v not in (None, "", [], {}))
    return round(100 * filled / len(data), 1)


# ---------- Main ----------
st.title("📄 Intelligent Document Extraction & Analysis System")
st.caption("Batch upload → extract → validate → analyze → compare → ask questions")

tab_upload, tab_data, tab_analytics, tab_compare, tab_ask = st.tabs(
    ["📤 Upload & Extract", "📊 Structured Data", "📈 Analytics", "🆚 Compare", "💬 Ask"]
)

# ---- Tab 1: Batch Upload & Extract ----
with tab_upload:
    uploaded_files = st.file_uploader(
        "Upload one or more documents (PDF, image, or TXT)",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) ready. Extract text, then run structured extraction individually or in batch.")

        col_a, col_b = st.columns([1, 1])
        process_all = col_a.button("⚡ Process All (extract text + structured fields)", use_container_width=True)
        clear_all = col_b.button("🗑️ Clear all documents", use_container_width=True)

        if clear_all:
            st.session_state.documents = {}
            st.rerun()

        for uf in uploaded_files:
            if uf.name not in st.session_state.documents:
                st.session_state.documents[uf.name] = {
                    "text": None, "structured_data": None, "confidence": None,
                    "summary": None, "schema": None, "processed_at": None,
                }

            doc = st.session_state.documents[uf.name]
            flagged = doc["confidence"] and any(
                v.get("confidence") == "low" for v in doc["confidence"].values()
            )
            card_class = "doc-card flagged" if flagged else "doc-card"
            st.markdown(f'<div class="{card_class}"><b>📄 {uf.name}</b></div>', unsafe_allow_html=True)

            c1, c2, c3 = st.columns([1, 1, 1])

            if c1.button(f"Extract text", key=f"text_{uf.name}"):
                with st.spinner(f"Extracting text from {uf.name}..."):
                    doc["text"] = extract_text_from_file(uf)
                st.success(f"Extracted {len(doc['text'])} characters")

            if c2.button(f"Get structured fields", key=f"struct_{uf.name}"):
                if not groq_api_key:
                    st.error("Enter your Groq API key in the sidebar.")
                elif not doc["text"]:
                    st.warning("Extract text first.")
                else:
                    try:
                        schema = json.loads(schema_text)
                        with st.spinner("Extracting structured data via Groq..."):
                            doc["structured_data"] = extract_structured_data(doc["text"], schema, groq_api_key, model_choice)
                            doc["schema"] = schema
                            doc["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if run_validation:
                            with st.spinner("Running confidence validation..."):
                                doc["confidence"] = validate_extraction(doc["text"], doc["structured_data"], groq_api_key, model_choice)
                        st.session_state.history.insert(0, {
                            "filename": uf.name, "time": doc["processed_at"], "model": model_choice
                        })
                        st.success("Structured extraction complete — see 'Structured Data' tab")
                    except json.JSONDecodeError:
                        st.error("Schema is not valid JSON.")
                    except Exception as e:
                        st.error(f"Extraction failed: {e}")

            if c3.button(f"Summarize", key=f"sum_{uf.name}"):
                if not groq_api_key:
                    st.error("Enter your Groq API key in the sidebar.")
                elif not doc["text"]:
                    st.warning("Extract text first.")
                else:
                    with st.spinner("Summarizing..."):
                        doc["summary"] = summarize_document(doc["text"], groq_api_key, model_choice)
                    st.success("Summary ready")

            if doc["text"]:
                with st.expander(f"View / search extracted text — {uf.name}"):
                    search_q = st.text_input("🔎 Highlight keyword", key=f"search_{uf.name}")
                    st.markdown(highlight_text(doc["text"][:6000], search_q), unsafe_allow_html=True)
                    if len(doc["text"]) > 6000:
                        st.caption("(showing first 6000 characters)")

            if doc["summary"]:
                with st.expander(f"Summary — {uf.name}"):
                    st.write(doc["summary"])

        if process_all:
            if not groq_api_key:
                st.error("Enter your Groq API key in the sidebar.")
            else:
                try:
                    schema = json.loads(schema_text)
                except json.JSONDecodeError:
                    st.error("Schema is not valid JSON.")
                    schema = None
                if schema:
                    progress = st.progress(0, text="Starting batch processing...")
                    for i, uf in enumerate(uploaded_files):
                        doc = st.session_state.documents[uf.name]
                        progress.progress((i) / len(uploaded_files), text=f"Processing {uf.name}...")
                        if not doc["text"]:
                            doc["text"] = extract_text_from_file(uf)
                        doc["structured_data"] = extract_structured_data(doc["text"], schema, groq_api_key, model_choice)
                        doc["schema"] = schema
                        doc["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if run_validation:
                            doc["confidence"] = validate_extraction(doc["text"], doc["structured_data"], groq_api_key, model_choice)
                        st.session_state.history.insert(0, {
                            "filename": uf.name, "time": doc["processed_at"], "model": model_choice
                        })
                    progress.progress(1.0, text="Done!")
                    st.success(f"Processed {len(uploaded_files)} document(s). See 'Structured Data' and 'Analytics' tabs.")

# ---- Tab 2: Structured Data ----
with tab_data:
    processed = {k: v for k, v in st.session_state.documents.items() if v["structured_data"]}
    if not processed:
        st.info("Upload documents and run 'Get structured fields' in the Upload tab.")
    else:
        selected_doc = st.selectbox("Select a document", list(processed.keys()))
        doc = processed[selected_doc]

        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Extracted Fields")
            if doc["confidence"]:
                for field, value in doc["structured_data"].items():
                    conf = doc["confidence"].get(field, {})
                    badge = confidence_badge_html(conf.get("confidence", "medium"))
                    note = conf.get("note", "")
                    note_html = f'<span style="color:#9a9ab0;font-size:0.8rem;"> — {note}</span>' if note else ""
                    st.markdown(f'{badge} <b>{field}</b>: {value}{note_html}', unsafe_allow_html=True)
            else:
                st.json(doc["structured_data"])

        with col2:
            st.subheader("Completeness")
            pct = field_completeness(doc["structured_data"])
            st.metric("Fields filled", f"{pct}%")
            if doc["confidence"]:
                low = sum(1 for v in doc["confidence"].values() if v.get("confidence") == "low")
                st.metric("Low-confidence fields", low)

        st.divider()
        st.subheader("Export")
        df = pd.json_normalize(doc["structured_data"])
        e1, e2, e3 = st.columns(3)
        with e1:
            st.download_button("⬇️ JSON", data=json.dumps(doc["structured_data"], indent=2),
                                file_name=f"{selected_doc}_extracted.json", mime="application/json", use_container_width=True)
        with e2:
            st.download_button("⬇️ CSV", data=df.to_csv(index=False),
                                file_name=f"{selected_doc}_extracted.csv", mime="text/csv", use_container_width=True)
        with e3:
            st.download_button("⬇️ Excel", data=to_excel_bytes(doc["structured_data"]),
                                file_name=f"{selected_doc}_extracted.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True)

# ---- Tab 3: Analytics ----
with tab_analytics:
    processed = {k: v for k, v in st.session_state.documents.items() if v["structured_data"]}
    if not processed:
        st.info("Process at least one document to see analytics.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Documents processed", len(processed))
        avg_completeness = round(sum(field_completeness(d["structured_data"]) for d in processed.values()) / len(processed), 1)
        m2.metric("Avg. field completeness", f"{avg_completeness}%")
        total_low = sum(
            sum(1 for v in d["confidence"].values() if v.get("confidence") == "low")
            for d in processed.values() if d["confidence"]
        )
        m3.metric("Total low-confidence flags", total_low)

        st.subheader("Field completeness by document")
        chart_df = pd.DataFrame({
            "Document": list(processed.keys()),
            "Completeness %": [field_completeness(d["structured_data"]) for d in processed.values()],
        }).set_index("Document")
        st.bar_chart(chart_df)

        conf_docs = {k: v for k, v in processed.items() if v["confidence"]}
        if conf_docs:
            st.subheader("Confidence breakdown by document")
            rows = []
            for name, d in conf_docs.items():
                counts = {"high": 0, "medium": 0, "low": 0}
                for v in d["confidence"].values():
                    counts[v.get("confidence", "medium")] = counts.get(v.get("confidence", "medium"), 0) + 1
                rows.append({"Document": name, **counts})
            conf_df = pd.DataFrame(rows).set_index("Document")
            st.bar_chart(conf_df)

# ---- Tab 4: Compare Documents ----
with tab_compare:
    processed = {k: v for k, v in st.session_state.documents.items() if v["structured_data"]}
    if len(processed) < 2:
        st.info("Process at least two documents to compare them (e.g. invoice vs. purchase order, resume vs. job description).")
    else:
        col1, col2 = st.columns(2)
        doc_a_name = col1.selectbox("Document A", list(processed.keys()), key="cmp_a")
        doc_b_name = col2.selectbox("Document B", [k for k in processed.keys() if k != doc_a_name], key="cmp_b")

        if st.button("🆚 Compare"):
            if not groq_api_key:
                st.error("Enter your Groq API key in the sidebar.")
            else:
                with st.spinner("Comparing documents..."):
                    result = compare_documents(
                        doc_a_name, processed[doc_a_name]["structured_data"],
                        doc_b_name, processed[doc_b_name]["structured_data"],
                        groq_api_key, model_choice,
                    )
                st.subheader("Summary")
                st.write(result.get("summary", ""))

                st.subheader("Differences")
                diffs = result.get("differences", [])
                if diffs:
                    diff_df = pd.DataFrame(diffs)
                    st.dataframe(diff_df, use_container_width=True)
                else:
                    st.success("No differences found.")

                matches = result.get("matches", [])
                if matches:
                    st.subheader("Matching fields")
                    st.write(", ".join(matches))

# ---- Tab 5: Ask the Document ----
with tab_ask:
    docs_with_text = {k: v for k, v in st.session_state.documents.items() if v["text"]}
    if not docs_with_text:
        st.info("Extract text from a document first (Upload tab).")
    else:
        active_doc = st.selectbox("Ask about which document?", list(docs_with_text.keys()))
        if active_doc not in st.session_state.chat_history:
            st.session_state.chat_history[active_doc] = []

        for msg in st.session_state.chat_history[active_doc]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        question = st.chat_input("Ask a question about this document...")
        if question:
            if not groq_api_key:
                st.error("Enter your Groq API key in the sidebar.")
            else:
                st.session_state.chat_history[active_doc].append({"role": "user", "content": question})
                with st.chat_message("user"):
                    st.write(question)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        answer = ask_document_question(
                            docs_with_text[active_doc]["text"], question, groq_api_key, model_choice
                        )
                        st.write(answer)
                st.session_state.chat_history[active_doc].append({"role": "assistant", "content": answer})
