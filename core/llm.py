# core/llm.py
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_TOKENS
import streamlit as st

# Global singleton - initialized only once when first requested
_llm = None


def get_llm():
    """
    Returns the same Gemini LLM instance throughout the application lifetime
    """
    global _llm

    if _llm is None:
        api_key = st.secrets["GEMINI_API_KEY"]

        if not api_key or len(api_key) < 20:
            st.error("Gemini API key is missing or invalid")
            st.stop()

        _llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=api_key,
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=GEMINI_MAX_TOKENS,
        )

    return _llm