import os
import pickle
import threading

import faiss
from sentence_transformers import SentenceTransformer

from config import FAISS_INDEX_PATH, CHUNKS_PATH, EMBEDDING_MODEL_NAME, TOP_K

_model = None
_index = None
_chunks = None
_lock = threading.Lock()


def warm_up():
    """Load the embedding model, FAISS index, and chunk texts into memory."""
    global _model, _index, _chunks
    with _lock:
        if _model is None:
            _model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        if _index is None:
            if not os.path.exists(FAISS_INDEX_PATH):
                raise RuntimeError(
                    f"No FAISS index found at '{FAISS_INDEX_PATH}'. "
                    "Run build_index.py first."
                )
            _index = faiss.read_index(FAISS_INDEX_PATH)

        if _chunks is None:
            if not os.path.exists(CHUNKS_PATH):
                raise RuntimeError(
                    f"No chunk store found at '{CHUNKS_PATH}'. "
                    "Run build_index.py first."
                )
            with open(CHUNKS_PATH, "rb") as f:
                _chunks = pickle.load(f)


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Return the top-k most relevant chunks as {"text": ..., "source": ...} dicts."""
    if _model is None or _index is None or _chunks is None:
        warm_up()

    query_vec = _model.encode([query]).astype("float32")
    distances, indices = _index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(_chunks):
            results.append(_chunks[idx])
    return results


def is_ready() -> bool:
    """Used by the /health endpoint - true once the model/index/chunks are loaded."""
    return _model is not None and _index is not None and _chunks is not None