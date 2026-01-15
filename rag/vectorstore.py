# rag/vectorstore.py
import os
import chromadb
from config.settings import CHROMA_COLLECTION_NAME, CHROMA_PATH
from data.school_knowledge_loader import load_all_school_documents

# Ensure directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

_client = None
_collection = None


def get_chroma_collection(reset: bool = False):
    """
    Get or (re)create Chroma collection with PDF content
    Set reset=True to force reload from PDFs (useful during development)
    """
    global _client, _collection

    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)

    if reset or _collection is None:
        # Optional: delete old collection to start fresh
        try:
            _client.delete_collection(CHROMA_COLLECTION_NAME)
        except:
            pass

        _collection = _client.create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

        # Load documents from PDFs
        docs = load_all_school_documents()
        
        if not docs:
            print("Warning: No documents loaded from PDFs!")
            return _collection

        # Add to Chroma
        texts = [d["text"] for d in docs]
        metadatas = [d["metadata"] for d in docs]
        ids = [f"{d['metadata']['source']}_chunk_{d['metadata']['chunk_id']}" for d in docs]

        _collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(texts)} chunks to collection '{CHROMA_COLLECTION_NAME}'")

    return _collection


def get_chroma_collection_readonly():
    """Use this in production / normal usage (don't recreate)"""
    return get_chroma_collection(reset=False)


def get_chroma_collection_writeonly():
    """Use this in production / normal usage (recreate)"""
    return get_chroma_collection(reset=True)