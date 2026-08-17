import os

#Paths
DATA_DIR = os.getenv("DATA_DIR", "data")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index/index.bin")
CHUNKS_PATH = os.getenv("CHUNKS_PATH", "faiss_index/chunks.pkl")

#Embedding model
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

#Chunking
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
MIN_CHUNK_SENTENCES = int(os.getenv("MIN_CHUNK_SENTENCES", "2"))
MAX_CHUNK_SENTENCES = int(os.getenv("MAX_CHUNK_SENTENCES", "12"))

#Retrieval
TOP_K = int(os.getenv("TOP_K", "3"))

#LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemini-3.6-flash")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))

#Server
PORT = int(os.getenv("PORT", "8000"))