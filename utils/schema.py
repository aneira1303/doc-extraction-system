"""
Default field-extraction schemas for common document types.
Users can edit these in the sidebar before running extraction.
"""

SCHEMA_TEMPLATES = {
    "Invoice": {
        "invoice_number": "Invoice or bill number",
        "invoice_date": "Date the invoice was issued",
        "due_date": "Payment due date",
        "vendor_name": "Name of the vendor/seller",
        "vendor_address": "Vendor's address",
        "customer_name": "Name of the customer/buyer",
        "line_items": "List of items with description, quantity, unit price, total",
        "subtotal": "Subtotal before tax",
        "tax_amount": "Tax amount",
        "total_amount": "Final total amount due",
        "currency": "Currency used",
    },
    "Resume": {
        "candidate_name": "Full name of candidate",
        "email": "Email address",
        "phone": "Phone number",
        "skills": "List of technical/professional skills",
        "education": "List of degrees, institutions, and years",
        "work_experience": "List of roles with company, title, duration, responsibilities",
        "certifications": "Any certifications listed",
        "total_years_experience": "Estimated total years of professional experience",
    },
    "Contract": {
        "contract_title": "Title of the contract/agreement",
        "parties": "Names of all parties involved",
        "effective_date": "Date the contract becomes effective",
        "expiration_date": "Date the contract expires, if any",
        "key_obligations": "Summary of major obligations for each party",
        "payment_terms": "Payment terms and amounts",
        "termination_clause": "Conditions under which the contract can be terminated",
        "governing_law": "Jurisdiction/governing law stated",
    },
    "Medical Report": {
        "patient_name": "Patient name",
        "date_of_report": "Date of the report",
        "diagnosis": "Diagnosis or findings",
        "medications": "Prescribed medications",
        "doctor_name": "Attending doctor's name",
        "recommendations": "Recommended follow-up or treatment",
    },
    "Generic / Custom": {
        "title": "Document title or subject",
        "date": "Any date mentioned",
        "key_entities": "Important names, organizations, or places mentioned",
        "key_points": "List of the most important points in the document",
        "summary": "One-paragraph summary",
    },
}
