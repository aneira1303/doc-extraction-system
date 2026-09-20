# 📄 Intelligent Document Extraction & Analysis System

LLM-powered document extraction and analysis tool built with **Streamlit** and the **Groq API**.

Upload invoices, resumes, contracts, medical reports, or any document — get back structured
JSON/CSV data, a summary, and can ask natural-language questions grounded in the document.

## Features
- 📤 **Batch multi-document upload**: process several files in one pass, or one at a time
- 🔍 **Structured field extraction**: schema-driven, JSON-mode Groq calls, editable per document type
- ✅ **Confidence validation pass**: a second LLM call fact-checks each extracted field against the source text and flags it high/medium/low confidence, with a reason for anything uncertain
- 📈 **Analytics dashboard**: field-completeness and confidence-breakdown charts across all processed documents
- 🆚 **Document comparison**: field-by-field diff between two documents (e.g. invoice vs. PO, resume vs. job description, contract v1 vs. v2)
- 🔎 **Search & highlight**: keyword search inside extracted raw text, highlighted inline
- 📝 **Summarization**: quick document overview
- 💬 **Document Q&A**: chat-style questions answered strictly from the uploaded document, with separate chat history per document
- 🕘 **Session history**: sidebar log of what's been processed, when, and with which model
- ⬇️ **Export**: download extracted data as JSON, CSV, or Excel (.xlsx)
- 🎨 **Black / blue / red theme**: dark UI with electric-blue accents and red alert/highlight states

## Folder Structure
```
doc-extraction-system/
├── app.py                  # Streamlit UI (entry point)
├── config.py                # (optional) central config / env loading
├── requirements.txt
├── .env.example
├── README.md
└── utils/
    ├── __init__.py
    ├── extractor.py         # PDF/image/text extraction (PyPDF2 + pytesseract)
    ├── groq_client.py       # Groq API wrapper (extraction, confidence validation, summary, Q&A, comparison)
    ├── schema.py             # Default field schemas per document type
    └── styling.py             # Black/blue/red custom CSS theme
```

## Setup

1. **Clone / copy the folder**, then install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **System dependency for OCR** (image extraction):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr

   # macOS
   brew install tesseract
   ```

3. **Set your Groq API key** — either via the app's sidebar input at runtime, or by copying
   `.env.example` to `.env` and filling it in:
   ```bash
   cp .env.example .env
   ```
   Get a free key at [console.groq.com](https://console.groq.com/keys).

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## How it works
1. **Ingestion** — `utils/extractor.py` pulls raw text out of the uploaded file (native PDF
   text layer, or OCR via `pytesseract` for images / scanned pages).
2. **Extraction** — `utils/groq_client.py` sends the text + a JSON schema to Groq with
   `response_format={"type": "json_object"}` so the model returns strict, parseable JSON.
3. **Analysis** — the same client exposes `summarize_document()` and
   `ask_document_question()` for summarization and grounded Q&A.
4. **Output** — the Streamlit UI renders the JSON, flattens it into a table, and offers
   JSON/CSV downloads.

## Extending
- Add new document types by adding an entry to `SCHEMA_TEMPLATES` in `utils/schema.py`.
- For scanned PDFs, add `pdf2image` + `pytesseract` page-by-page OCR in `extractor.py`.
- Swap in a vector DB (e.g. Chroma/FAISS) in front of `ask_document_question()` for
  multi-document RAG instead of single-document Q&A.
- Add authentication / multi-user storage if deploying beyond local/demo use.

## Models supported (Groq)
- `openai/gpt-oss-120b` (best quality — replaces the deprecated llama-3.3-70b-versatile)
- `openai/gpt-oss-20b` (fastest — replaces the deprecated llama-3.1-8b-instant)
- `qwen/qwen3.6-27b` (mid-size alternative)

> Groq deprecated `llama-3.1-8b-instant`, `llama-3.3-70b-versatile`, and `mixtral-8x7b-32768`
> (the latter much earlier). If you hit a `model_not_found` / 404 error, check
> [console.groq.com/docs/models](https://console.groq.com/docs/models) for the current list —
> Groq rotates models fairly often.
