import pickle
import faiss
import numpy as np

from config import FAISS_PATH


INDEX_FILE = FAISS_PATH / "index.faiss"
METADATA_FILE = FAISS_PATH / "metadata.pkl"


class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []

    def save(self):
        FAISS_PATH.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(INDEX_FILE))

        with open(METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(str(INDEX_FILE))

        with open(METADATA_FILE, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, embedding, k=3):
        embedding = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(embedding, k)

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])

        return results