# Hybrid RAG + Fine-Tuned Text-to-SQL Assistant

A local AI assistant that answers questions from both PDF documents and a SQL Server database. The project combines document retrieval, a fine-tuned Text-to-SQL model, SQL validation, and an Ollama-powered response layer to support document, database, and hybrid questions from one command-line interface.

## Highlights

- Routes each question to the right path: document RAG, SQL, or hybrid.
- Retrieves PDF context from a FAISS vector index built with `BAAI/bge-small-en-v1.5` embeddings.
- Uses a fine-tuned local T5-style model to translate natural language into SQL.
- Validates generated SQL before execution to block dangerous statements.
- Executes database queries through SQL Server using `pyodbc`.
- Uses Ollama with `llama3` to generate final natural-language answers.
- Returns document sources with page numbers for document-based answers.

## Architecture

```mermaid
flowchart LR
    User["User Question"] --> Router["Question Router"]

    Router -->|"document"| Retriever["FAISS Retriever"]
    Router -->|"sql"| SQLAgent["Fine-Tuned Text-to-SQL Agent"]
    Router -->|"hybrid"| Hybrid["Hybrid Orchestrator"]

    Retriever --> Docs["PDF Chunks + Metadata"]
    Docs --> DocumentPrompt["Document Prompt"]
    DocumentPrompt --> Ollama["Ollama LLM"]

    SQLAgent --> Generator["Local T5 SQL Generator"]
    Generator --> Validator["SQL Cleaner + Validator"]
    Validator --> Database["SQL Server Database"]
    Database --> SQLResult["Tabular Result"]

    Hybrid --> Retriever
    Hybrid --> SQLAgent
    SQLResult --> HybridPrompt["Hybrid Prompt"]
    Docs --> HybridPrompt
    HybridPrompt --> Ollama

    Ollama --> Answer["Final Answer"]
```

## Runtime Flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as app.py
    participant R as Router
    participant V as FAISS
    participant S as SQL Agent
    participant D as SQL Server
    participant L as Ollama

    U->>A: Ask a question
    A->>R: Classify question intent

    alt Document question
        R-->>A: document
        A->>V: Retrieve top PDF chunks
        V-->>A: Context + sources
        A->>L: Ask with document context
        L-->>A: Grounded answer
    else SQL question
        R-->>A: sql
        A->>S: Generate SQL
        S->>S: Clean and validate SQL
        S->>D: Execute query
        D-->>S: Rows
        S-->>A: Answer + SQL
    else Hybrid question
        R-->>A: hybrid
        A->>V: Retrieve document context
        A->>S: Generate and run SQL
        S->>D: Execute query
        D-->>S: Rows
        A->>L: Combine document and database context
        L-->>A: Final answer
    end

    A-->>U: Print answer
```

## Data Pipeline

```mermaid
flowchart TB
    PDFs["PDF files in data/documents"] --> Loader["PyPDFDirectoryLoader"]
    Loader --> Splitter["RecursiveCharacterTextSplitter"]
    Splitter --> Embeddings["SentenceTransformer Embeddings"]
    Embeddings --> Index["FAISS Index"]
    Splitter --> Metadata["Chunk Metadata"]
    Index --> Storage["data/faiss_index/index.faiss"]
    Metadata --> MetadataFile["data/faiss_index/metadata.pkl"]
```

## Project Structure

```text
.
├── app.py                  # CLI entry point and orchestration
├── config.py               # Model, database, and retrieval settings
├── core/
│   ├── llm.py              # Ollama LLM loader
│   ├── prompts.py          # Document and hybrid prompts
│   └── router.py           # Question routing logic
├── rag/
│   ├── ingest.py           # PDF ingestion and FAISS index builder
│   ├── embeddings.py       # SentenceTransformer embedding model
│   ├── retriever.py        # Query-time vector retrieval
│   └── vector_store.py     # FAISS persistence wrapper
├── sql/
│   ├── db.py               # SQL Server connection
│   ├── schema.py           # Database schema reference
│   ├── sql_agent.py        # Fine-tuned Text-to-SQL inference and execution
│   └── validator.py        # SQL cleanup and safety checks
├── data/
│   ├── documents/          # Source PDFs
│   └── faiss_index/        # Persisted vector index
└── models/                 # Fine-tuned local Text-to-SQL model
```

## Requirements

- Python 3.11 or newer
- SQL Server with ODBC Driver 17
- Ollama installed locally
- `llama3` available in Ollama
- A fine-tuned model saved in `models/`
- PDF files in `data/documents/`

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Pull the Ollama model if needed:

```bash
ollama pull llama3
```

## Configuration

Update [config.py](config.py) for your local environment:

```python
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama3"
TOP_K = 3
MAX_SQL_ROWS = 20
CONNECTION_STRING = "..."
```

The current database connection targets a local SQL Server database named `university`.

## Build The Document Index

Add PDFs to `data/documents/`, then build the FAISS index:

```bash
python rag/ingest.py
```

This creates:

```text
data/faiss_index/index.faiss
data/faiss_index/metadata.pkl
```

## Run The Assistant

```bash
python app.py
```

Example prompts:

```text
What are the rules in the Monopoly document?
Show the students enrolled in computer science.
Compare the document rules with the database course information.
```

## SQL Safety

Generated SQL is cleaned and checked before execution. The validator blocks high-risk commands such as:

```text
DROP, ALTER, TRUNCATE, EXEC, EXECUTE, CREATE
```

`UPDATE` and `DELETE` statements are also blocked unless they include a `WHERE` clause.

