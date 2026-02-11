# rag-chatbot-with-ollama
This project is a Hybrid RAG (Retrieval-Augmented Generation) System designed to bridge the gap between unstructured documents and structured databases. By utilizing Ollama (Llama 3) and ChromaDB, it allows users to query both PDF files and live SQL Server data through a single conversational interface.

### File Analysis

* **`get_embedding_function.py`**: The foundation. It initializes the `nomic-embed-text` model via Ollama to ensure consistent vectorization across ingestion and retrieval.
* **`populate_database.py`**: The PDF pipeline. It handles loading documents, splitting text into manageable chunks with overlap, and performing incremental updates to the Chroma vector store.
* **`DataBase.py`**: The SQL pipeline. It connects to a local SQL Server, extracts both schema metadata and row content, and indexes them into a separate vector store.
* **`query_data.py`**: The "brain" of the project. It performs a dual-search across both the document and SQL vector stores, reranks results, maintains conversation memory, and queries **Llama 3** for the final answer.
* **`rag_with_ollama.py`**: A clean, terminal-based CLI for interacting with the agent, featuring session-based chat history.
* **`rag_ui.py`**: A user-friendly desktop interface built with `tkinter`, using multi-threading to ensure the UI stays responsive while the AI is "thinking."

---

### GitHub README.md

```markdown
# Hybrid RAG Agent: PDF & SQL Server Integration

A sophisticated Retrieval-Augmented Generation (RAG) system that combines unstructured PDF data with structured SQL Server data. This agent uses **Ollama (Llama 3)** for generation and **ChromaDB** for vector storage, providing a unified conversational interface to query both documents and databases.

## 🚀 Features
* **Dual-Source Retrieval**: Searches across both PDF document chunks and SQL database schemas/rows.
* **Interactive UI & CLI**: Choose between a modern multi-threaded Tkinter GUI or a lightweight terminal interface.
* **Persistent Memory**: Maintains a sliding window of chat history (last 10 messages) for contextual follow-up questions.
* **Source Attribution**: Clearly identifies which files or database tables were used to generate the response.
* **Incremental Ingestion**: Smart ID tracking in the PDF pipeline ensures only new content is added to the vector store.

## 🛠️ Tech Stack
* **LLM**: Ollama (Llama 3)
* **Embeddings**: nomic-embed-text
* **Orchestration**: LangChain
* **Vector Database**: ChromaDB
* **Database**: Microsoft SQL Server (pyodbc)
* **Frontend**: Tkinter (Python Standard Library)

## 📋 Prerequisites
1.  **Ollama**: Install [Ollama](https://ollama.ai/) and pull the required models:
    ```bash
    ollama pull llama3
    ollama pull nomic-embed-text
    ```
2.  **SQL Server**: Ensure your SQL Server is running and update the `CONN_STR` in `DataBase.py` with your credentials.
3.  **Dependencies**:
    ```bash
    pip install langchain langchain-community langchain-chroma pyodbc
    ```

## 📂 Project Structure
* `populate_database.py`: Processes PDFs in the `/data` folder into vectors.
* `DataBase.py`: Connects to SQL Server and indexes table structures and records.
* `query_data.py`: Logic for similarity search and LLM prompting.
* `rag_ui.py`: The graphical user interface script.
* `rag_with_ollama.py`: The command-line interface script.

## ⚙️ Setup & Usage

### 1. Ingest Data
First, populate your vector databases. Place your PDFs in a folder named `data/` and run:
```bash
# Ingest PDFs
python populate_database.py --reset

# Ingest SQL Data
python DataBase.py

```

### 2. Run the Agent

You can start the agent in your preferred mode:

**Desktop GUI:**

```bash
python rag_ui.py

```

**Terminal CLI:**

```bash
python rag_with_ollama.py

```

## 📝 License

This project is open-source and available for educational purposes.

```
pip install -r requirements.txt
