# rag/retriever.py
from langchain_core.runnables import RunnableLambda
from rag.vectorstore import get_chroma_collection_readonly


def retrieve_docs(question: str) -> str:
    collection = get_chroma_collection_readonly()
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    docs = results["documents"][0]
    return "\n\n".join(docs) if docs else "No relevant school information found."


retriever = RunnableLambda(retrieve_docs)