from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_PATH = BASE_DIR / "data" / "documents"
FAISS_PATH = BASE_DIR / "data" / "faiss_index"
MODEL_PATH = BASE_DIR / "models"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama3"

TOP_K = 3
MAX_SQL_ROWS = 20

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-TCRP0DB;"
    "DATABASE=university;"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)