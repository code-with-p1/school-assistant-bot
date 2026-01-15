# data/school_knowledge_loader.py
import os
from pathlib import Path
import fitz  # PyMuPDF - fast and reliable
from typing import List, Dict

PDF_FOLDER = Path(__file__).parent / "school_docs"


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract clean text from PDF using PyMuPDF"""
    text = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text.append(page.get_text("text"))
        doc.close()
        return "\n\n".join(text).strip()
    except Exception as e:
        print(f"Error reading {pdf_path.name}: {e}")
        return ""


def load_all_school_documents() -> List[Dict]:
    """
    Returns list of documents ready for Chroma:
    [
        {"text": "...full text...", "metadata": {"source": "filename.pdf", "page": 0}},
        ...
    ]
    """
    documents = []

    if not PDF_FOLDER.exists():
        print(f"PDF folder not found: {PDF_FOLDER}")
        return documents

    pdf_files = list(PDF_FOLDER.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files in {PDF_FOLDER}")

    for pdf_path in pdf_files:
        full_text = extract_text_from_pdf(pdf_path)
        if not full_text:
            continue

        # Very simple chunking - you can improve with langchain text splitters later
        # Here we split by paragraphs (roughly 500-800 chars chunks)
        paragraphs = [p.strip() for p in full_text.split("\n\n") if p.strip()]
        
        for i, para in enumerate(paragraphs):
            if len(para) < 50:  # skip very short fragments
                continue
                
            documents.append({
                "text": para,
                "metadata": {
                    "source": pdf_path.name,
                    "chunk_id": i,
                    "file_path": str(pdf_path)
                }
            })

    print(f"Extracted {len(documents)} text chunks from PDFs")
    return documents