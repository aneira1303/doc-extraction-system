"""
Groq LLM client wrapper.
Handles: structured field extraction (JSON mode), confidence validation,
summarization, Q&A over document text, and cross-document comparison.
"""

import json
from groq import Groq


def _get_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def _chat_json(client, model, system_prompt, user_prompt, temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def extract_structured_data(text: str, schema: dict, api_key: str, model: str) -> dict:
    """Send document text + a target schema to Groq, ask for strict JSON output."""
    client = _get_client(api_key)

    system_prompt = (
        "You are a precise document extraction engine. "
        "Extract the requested fields from the document text. "
        "Respond ONLY with valid JSON matching the given schema's keys. "
        "If a field is not present in the document, set its value to null. "
        "Do not include any explanation, markdown formatting, or code fences."
    )
    user_prompt = f"""
Schema (keys to extract, values describe what to extract for each):
{json.dumps(schema, indent=2)}

Document text:
\"\"\"
{text[:15000]}
\"\"\"

Return a single JSON object with exactly these keys, populated from the document.
"""
    return _chat_json(client, model, system_prompt, user_prompt)


def validate_extraction(text: str, extracted_data: dict, api_key: str, model: str) -> dict:
    """
    Advanced feature: confidence / self-validation pass.
    Asks the LLM to re-check each extracted field against the source text and
    assign a confidence level, flagging anything uncertain, inferred, or missing.

    Returns: {field_name: {"confidence": "high"|"medium"|"low", "note": "..."}}
    """
    client = _get_client(api_key)

    system_prompt = (
        "You are a meticulous fact-checker for document extraction results. "
        "For each field in the provided extracted data, verify it against the source "
        "document text. Respond ONLY with valid JSON: an object whose keys match the "
        "extracted data's keys, and whose values are objects with 'confidence' "
        "('high', 'medium', or 'low') and 'note' (a short reason, especially for "
        "medium/low confidence — e.g. 'not found in text', 'inferred, not explicit', "
        "'ambiguous date format'). No markdown, no extra text."
    )
    user_prompt = f"""
Extracted data to verify:
{json.dumps(extracted_data, indent=2)}

Source document text:
\"\"\"
{text[:15000]}
\"\"\"

Return the confidence JSON object now.
"""
    return _chat_json(client, model, system_prompt, user_prompt)


def summarize_document(text: str, api_key: str, model: str) -> str:
    """Generate a concise summary of the document."""
    client = _get_client(api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes clear, concise document summaries (5-8 sentences), covering purpose, key facts, and any action items."},
            {"role": "user", "content": f"Summarize this document:\n\n{text[:15000]}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def ask_document_question(text: str, question: str, api_key: str, model: str) -> str:
    """Answer a user question grounded strictly in the provided document text."""
    client = _get_client(api_key)
    system_prompt = (
        "You are a document Q&A assistant. Answer ONLY using information found in the "
        "provided document text. If the answer is not in the document, say so clearly "
        "instead of guessing."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document:\n\"\"\"\n{text[:15000]}\n\"\"\"\n\nQuestion: {question}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


def compare_documents(doc_a_name: str, data_a: dict, doc_b_name: str, data_b: dict, api_key: str, model: str) -> dict:
    """
    Advanced feature: compare two documents' extracted structured data.
    Useful for contract redlines, invoice-vs-PO matching, resume-vs-JD matching, etc.

    Returns: {"differences": [...], "matches": [...], "summary": "..."}
    """
    client = _get_client(api_key)

    system_prompt = (
        "You compare two structured extractions from different documents and report "
        "differences and matches field by field. Respond ONLY with valid JSON: "
        "{\"differences\": [{\"field\": str, \"doc_a_value\": ..., \"doc_b_value\": ..., "
        "\"significance\": \"high\"|\"medium\"|\"low\"}], "
        "\"matches\": [field names that are the same or equivalent], "
        "\"summary\": \"2-3 sentence plain-English summary of how the documents differ\"}"
    )
    user_prompt = f"""
Document A ("{doc_a_name}"):
{json.dumps(data_a, indent=2)}

Document B ("{doc_b_name}"):
{json.dumps(data_b, indent=2)}

Compare them field by field and return the JSON now.
"""
    return _chat_json(client, model, system_prompt, user_prompt)
