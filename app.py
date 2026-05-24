from core.router import route_question
from core.prompts import DOCUMENT_PROMPT
from core.prompts import HYBRID_PROMPT
from core.llm import get_llm

from rag.retriever import retrieve
from sql.sql_agent import SQLAgent


llm = get_llm()
sql_agent = SQLAgent()


def answer_document_question(question):
    results = retrieve(question)

    context = "\n\n".join(item["text"] for item in results)
    prompt = DOCUMENT_PROMPT.format(context= context, question= question)
    answer = llm.invoke(prompt)

    sources = []

    for item in results:
        source = item["source"]
        page = item["page"] + 1

        sources.append(f"{source} (Page {page})")

    return answer, list(set(sources))

def answer_hybrid_question(question):
    doc_results = retrieve(question)

    document_context = "\n\n".join(item["text"] for item in doc_results)
    sql_result = sql_agent.ask(question)
    prompt = HYBRID_PROMPT.format(document_context= document_context, database_context= sql_result["answer"], question= question)

    answer = llm.invoke(prompt)
    return answer

def main():
    print("Hybrid RAG + SQL System Started")
    print("Type 'exit' to quit")

    while True:
        question = input("\nUser: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            break

        route = route_question(question)

        try:
            if route == "document":
                answer, sources = answer_document_question(question)

                print("\nAI:")
                print(answer)

                print("\nSources:")
                for source in sources:
                    print(source)

            elif route == "sql":
                result = sql_agent.ask(question)

                print("\nAI:")
                print(result["answer"])

                print("\nSQL:")
                print(result["sql"])

            else:
                answer = answer_hybrid_question(question)

                print("\nAI:")
                print(answer)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()