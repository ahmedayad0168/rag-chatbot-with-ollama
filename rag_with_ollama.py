import time
from query_data import query_rag

print("--- RAG Q&A System Initialized (type 'exit' to quit) ---")
    
chat_history = []

while True:
    try:
        question = input("\nUser: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        if not question:
            continue

        start_time = time.time()

        response, sources = query_rag(question, chat_history)

        end_time = time.time()

        print("-" * 30)
        print(f"AI: {response}")
        if sources:
            print(f"Sources: {', '.join(sources)}")
        print(f"(Response time: {end_time - start_time:.2f}s)")
        print("-" * 30)

        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": response})

        if len(chat_history) > 10:
            chat_history = chat_history[-10:]

    except KeyboardInterrupt:
        print("\nSession ended.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")




# =============================================================================================================
# =============================================================================================================

# def ask_question(question: str, index: int):
#     print(f"\n=== Question {index} ===")
#     print(f"{question}\n")
#     response_text = query_rag(question)
#     print("=" * 50)
#     return response_text

# questions = [
#     "What is the main objective of Monopoly?",
#     "How much money does each player receive at the start of the game in classic rules?",
#     "When can a player start using the Speed Die?",
#     'What happens if you roll a "Bus" on the Speed Die?',
#     "What happens if you land on an unowned property?",
#     "How does the Bank handle mortgages?",
#     "What is the rule for building houses evenly in a color group?",
#     "How is rent affected if you own all properties in a color group?",
#     "Can you collect rent on a mortgaged property?",
#     "What should you do if you draw a 'Get Out of Jail Free' card?",
#     "How are Chance and Community Chest cards returned after use?",
#     "How can a player get out of jail?",
#     "What happens if a player throws doubles three times in succession?",
#     "What must a player do if they owe more money than they can pay to another player?",
#     "What happens if a player owes the Bank more than they can pay?",
#     "What happens when you land on Free Parking?",
#     "How much do you collect when passing 'GO'?"
# ]

# answers = {}

# for i, q in enumerate(questions, start= 1):
#     answers[q] = ask_question(q, i)
#     time.sleep(0.5)  
