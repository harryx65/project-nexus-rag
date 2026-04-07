from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"
CHROMA_FOLDER = BASE_DIR / "storage" / "chroma"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_LLM_REPO = "mistralai/Mistral-7B-Instruct-v0.3"
