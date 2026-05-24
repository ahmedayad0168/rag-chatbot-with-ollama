import faiss
import numpy as np

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import DOCUMENTS_PATH
from rag.embeddings import get_embedding_model
from rag.vector_store import VectorStore


CHUNK_SIZE = 400
CHUNK_OVERLAP = 50


def load_documents():
    loader = PyPDFDirectoryLoader(str(DOCUMENTS_PATH))
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size= CHUNK_SIZE, chunk_overlap= CHUNK_OVERLAP)
    return splitter.split_documents(documents)


def build_index():
    print("Loading documents...")
    documents = load_documents()

    print("Splitting documents...")
    chunks = split_documents(documents)

    model = get_embedding_model()

    texts = [chunk.page_content for chunk in chunks]

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    store = VectorStore()
    store.index = index

    for chunk in chunks:
        store.metadata.append({
            "text": chunk.page_content,
            "source": chunk.metadata.get("source", "Unknown"),
            "page": chunk.metadata.get("page", 0)
        })

    store.save()

    print("FAISS index created successfully.")


if __name__ == "__main__":
    build_index()