import os
import shutil
import argparse
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from get_embedding_function import get_embedding_function 

DATA_PATH = "data"      
CHROMA_PATH = "chroma"  


def load_documents(data_path: str) -> list[Document]:
    loader = PyPDFDirectoryLoader(data_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {data_path}")
    return documents


def split_documents(documents: list[Document], chunk_size= 800, chunk_overlap= 80) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= chunk_size,
        chunk_overlap= chunk_overlap,
        length_function= len,
        is_separator_regex= False
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def assign_chunk_ids(chunks: list[Document]) -> list[Document]:
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", 0)
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

    return chunks


def add_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory= CHROMA_PATH, embedding_function= get_embedding_function())

    chunks = assign_chunk_ids(chunks)

    try:
        existing_items = db._collection.get() 
        existing_ids = set(existing_items["ids"])
    except Exception:
        existing_ids = set()

    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"Adding {len(new_chunks)} new chunks to the database...")
        db.add_documents(new_chunks, ids= [chunk.metadata["id"] for chunk in new_chunks])
        db.persist()
        print("Database updated successfully!")
    else:
        print("No new chunks to add. Database is up-to-date.")


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Database cleared.")


def main(reset_db= False):
    if reset_db:
        clear_database()

    documents = load_documents(DATA_PATH)
    chunks = split_documents(documents)
    add_to_chroma(chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Build or update Chroma RAG database.")
    parser.add_argument("--reset", action= "store_true", help= "Reset the database before building.")
    args = parser.parse_args()

    main(reset_db= args.reset)
