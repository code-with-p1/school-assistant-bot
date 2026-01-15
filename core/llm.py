# core/llm.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
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

def get_hf_llm():
    """
    Returns the same HuggingFace LLM instance throughout the application lifetime
    """
    global _llm

    if _llm is None:
        api_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

        if not api_key or len(api_key) < 37:
            st.error("HuggingFace API key is missing or invalid")
            st.stop()

        llm = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-7B-Instruct",
            task="text-generation",
            temperature=0.8,
            top_p=0.95,
            max_new_tokens=512,
            huggingfacehub_api_token=api_key,
        )

        _llm = ChatHuggingFace(llm=llm)

    print("\n\n HF LLM Called")
    return _llm