import os
import glob
import pickle
import numpy as np
import faiss
import nltk
from sentence_transformers import SentenceTransformer

from config import (
    DATA_DIR,
    FAISS_INDEX_PATH,
    CHUNKS_PATH,
    EMBEDDING_MODEL_NAME,
    SIMILARITY_THRESHOLD,
    MIN_CHUNK_SENTENCES,
    MAX_CHUNK_SENTENCES,
)

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


def load_documents(data_dir: str) -> list[tuple[str, str]]:
    """Return a list of (filename, text) tuples for every .txt/.md file."""
    paths = glob.glob(os.path.join(data_dir, "**", "*.txt"), recursive=True)
    paths += glob.glob(os.path.join(data_dir, "**", "*.md"), recursive=True)

    documents = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            filename = os.path.relpath(path, data_dir)
            documents.append((filename, f.read()))
    return documents


def split_into_sentences(text: str) -> list[str]:
    from nltk.tokenize import sent_tokenize
    cleaned = " ".join(text.split())
    return sent_tokenize(cleaned)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def semantic_chunk(sentences: list[str], sentence_embeddings: np.ndarray) -> list[str]:
    if not sentences:
        return []

    chunks = []
    current_sentences = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = cosine_sim(sentence_embeddings[i - 1], sentence_embeddings[i])

        should_break = (
            sim < SIMILARITY_THRESHOLD and len(current_sentences) >= MIN_CHUNK_SENTENCES
        ) or len(current_sentences) >= MAX_CHUNK_SENTENCES

        if should_break:
            chunks.append(" ".join(current_sentences))
            current_sentences = [sentences[i]]
        else:
            current_sentences.append(sentences[i])

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks


def build_index():
    print(f"Loading documents from '{DATA_DIR}/'...")
    documents = load_documents(DATA_DIR)
    if not documents:
        raise RuntimeError(f"No .txt or .md files found in '{DATA_DIR}/'. Add source documents first.")
    print(f"Loaded {len(documents)} document(s).")

    print(f"Loading embedding model '{EMBEDDING_MODEL_NAME}'...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Splitting into sentences and semantic chunking...")
    # Each entry: {"text": chunk_text, "source": filename}
    all_chunks: list[dict] = []
    for filename, doc_text in documents:
        sentences = split_into_sentences(doc_text)
        if not sentences:
            continue
        sentence_embeddings = model.encode(sentences, convert_to_numpy=True)
        doc_chunks = semantic_chunk(sentences, sentence_embeddings)
        for chunk_text in doc_chunks:
            all_chunks.append({"text": chunk_text, "source": filename})

    print(f"Created {len(all_chunks)} semantic chunk(s) across {len(documents)} document(s).")

    print("Generating chunk-level embeddings...")
    chunk_texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(chunk_texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"Saved FAISS index to '{FAISS_INDEX_PATH}' ({index.ntotal} vectors).")

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)
    print(f"Saved {len(all_chunks)} chunk(s) (with source filenames) to '{CHUNKS_PATH}'.")

    print("Done.")


if __name__ == "__main__":
    build_index()