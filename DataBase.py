import os
import shutil
import pyodbc
from langchain_core.documents import Document
from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-TCRP0DB;"
    "DATABASE=university;"
    "Trusted_Connection=yes;"
    )

CHROMA_DIR = "chromadb"

def load_data():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        """)

    tables = [row[0] for row in cursor.fetchall()]
    print("Tables found:", tables)

    docs = []

    for table in tables:
        print(f"Reading table: {table}")

        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            """)

        columns_info = cursor.fetchall()
        schema_text = ", ".join(f"{col} ({dtype})" for col, dtype in columns_info)

        docs.append(Document(page_content=f"Table {table} has columns: {schema_text}", metadata={"type": "table_summary", "table": table}))

        cursor.execute(f"SELECT * FROM {table}")
        columns = [col[0] for col in cursor.description]

        for row in cursor.fetchall():
            row_text = " | ".join(f"{col}: {val}" for col, val in zip(columns, row))
            docs.append(Document(page_content=f"Table: {table}\n{row_text}", metadata={"type": "row", "table": table}))

    conn.close()
    return docs

def rebuild_vector_store(docs):
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)  

    embeddings = get_embedding_function()

    vectordb = Chroma.from_documents(documents= docs, embedding= embeddings, persist_directory= CHROMA_DIR)

    return vectordb

print("Loading data from SQL Server...")
docs = load_data()

print("Building vector DB...")
vectordb = rebuild_vector_store(docs)