from langchain_chroma import Chroma
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"      # documents
CHROMA_DIR = "chromadb"     # sql data

PROMPT_TEMPLATE = """
Use the context and chat history to answer.

Chat History:
{chat_history}

Context:
{context}

---

Answer the question: {question}
"""

def query_rag(query_text: str, chat_history=""):
    embedding_function = get_embedding_function()

    doc_db = Chroma(persist_directory= CHROMA_PATH, embedding_function= embedding_function)

    sql_db = Chroma(persist_directory= CHROMA_DIR, embedding_function= embedding_function)

    doc_results = doc_db.similarity_search_with_score(query_text, k= 5)
    sql_results = sql_db.similarity_search_with_score(query_text, k= 5)

    all_results = doc_results + sql_results
    all_results.sort(key=lambda x: x[1])  

    top_results = all_results[:7]  

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in top_results])

    prompt = PROMPT_TEMPLATE.format(chat_history= chat_history, context= context_text, question= query_text)

    model = Ollama(model= "llama3")
    response_text = model.invoke(prompt)

    sources = []
    for doc, _ in top_results:
        source_path = doc.metadata.get("source", "unknown")
        file_name = source_path.split("/")[-1].split("\\")[-1]
        page = doc.metadata.get("page", None)
        
        source_label = f"{file_name}"
        if page is not None:
            source_label += f" (Page {page + 1})" 
        sources.append(source_label)

    return response_text, list(set(sources))
