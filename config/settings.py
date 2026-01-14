# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Model configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 1200

# Chroma
CHROMA_COLLECTION_NAME = "school_knowledge_v1"
CHROMA_PATH = str(BASE_DIR / "chroma_db")  # persistent folder (optional)