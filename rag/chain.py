# rag/chain.py
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from core.llm import get_llm, get_hf_llm
from core.prompt_templates import SCHOOL_ASSISTANT_PROMPT
from rag.retriever import retriever


def get_rag_chain():
    """
    Returns fresh RAG chain every time.
    Chains are very lightweight → caching usually causes more problems than benefits.
    """
    llm = get_hf_llm()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | SCHOOL_ASSISTANT_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain