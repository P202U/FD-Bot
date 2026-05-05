import os


class Config:
    # Folders
    DATA_DIR = "data"
    PROCESSED_DIR = "processed"
    VECTOR_STORE_DIR = "vector_store"

    # Files
    KNOWLEDGE_BASE_MD = os.path.join(PROCESSED_DIR, "knowledge_base.md")
    FAISS_INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index")

    # Models
    # Using a local embedding model that doesn't need internet
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "gemma4:e2b"


# Initialize folders
for folder in [Config.DATA_DIR, Config.PROCESSED_DIR, Config.VECTOR_STORE_DIR]:
    os.makedirs(folder, exist_ok=True)
