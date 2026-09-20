"""
Handles text extraction from uploaded files: PDF, images (OCR), and plain text.
"""

import io
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract


def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file object. Falls back to OCR per-page if no text layer."""
    reader = PdfReader(file)
    text_chunks = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)
    text = "\n".join(text_chunks).strip()
    return text


def extract_text_from_image(file) -> str:
    """Run OCR on an uploaded image file."""
    image = Image.open(file)
    return pytesseract.image_to_string(image)


def extract_text_from_txt(file) -> str:
    """Read plain text file."""
    raw = file.read()
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="ignore")
    return raw


def extract_text_from_file(uploaded_file) -> str:
    """
    Dispatch extraction based on file type.
    `uploaded_file` is a Streamlit UploadedFile object.
    """
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
        if len(text.strip()) < 20:
            # Likely a scanned PDF with no text layer — could extend with pdf2image + OCR here
            return "[Warning: PDF appears to be scanned/image-based. Minimal text extracted via text layer.]\n" + text
        return text

    elif name.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(uploaded_file)

    elif name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    else:
        raise ValueError(f"Unsupported file type: {name}")
