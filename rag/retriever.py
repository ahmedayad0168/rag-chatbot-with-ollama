from rag.embeddings import get_embedding_model
from rag.vector_store import VectorStore
from config import TOP_K


store = VectorStore()
store.load()
model = get_embedding_model()

def retrieve(query, k=TOP_K):
    if store is None:
        raise RuntimeError("FAISS index not loaded. Run ingest.py to build it first.")

    embedding = model.encode(query)
    return store.search(embedding, k=k)