# rag/vectorstore.py
import os
import chromadb
from config.settings import CHROMA_COLLECTION_NAME, CHROMA_PATH
from data.school_knowledge import SCHOOL_DOCUMENTS

# Ensure directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

_client = None
_collection = None


def get_chroma_collection():
    global _client, _collection

    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)

    if _collection is None:
        try:
            _collection = _client.get_collection(CHROMA_COLLECTION_NAME)
        except chromadb.errors.NotFoundError:
            # This is the correct exception type in current Chroma versions
            _collection = _client.create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            _collection.add(
                documents=SCHOOL_DOCUMENTS,
                ids=[f"doc_{i}" for i in range(len(SCHOOL_DOCUMENTS))]
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chroma collection: {str(e)}")

    return _collection