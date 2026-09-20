"""
Optional central config. Loads defaults from environment variables (.env).
The Streamlit sidebar can still override these at runtime.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
MAX_CHARS_PER_REQUEST = 15000  # truncate long documents before sending to the LLM
