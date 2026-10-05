from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_model():
    # CPU keeps this small lab usable without a GPU. Never execute remote model code.
    return SentenceTransformer(MODEL, device="cpu", trust_remote_code=False)


def rank(query_vector, document_vectors, top_k):
    if top_k < 1:
        raise ValueError("top-k must be positive")
    # Unit-length vectors: dot product equals cosine similarity.
    scores = document_vectors @ query_vector
    return [(int(i), float(scores[i])) for i in np.argsort(-scores)[:top_k]]


def load_chunks(directory):
    chunks = []
    for path in sorted(directory.glob("*.md")):
        for number, paragraph in enumerate(path.read_text(encoding="utf-8").split("\n\n"), 1):
            if paragraph.strip():
                chunks.append({"source": f"{path.name}#{number}", "text": paragraph.strip()})
    if not chunks:
        raise ValueError("No Markdown paragraphs found in the document directory")
    return chunks
