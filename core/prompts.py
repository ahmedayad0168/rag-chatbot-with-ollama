DOCUMENT_PROMPT = """
Answer based on your understanding of the available context.

If the answer is not found, say:
'I could not find that information in the documents.'

Context:
{context}

Question:
{question}

Answer:
"""


HYBRID_PROMPT = """
Answer the question using BOTH:

1. Document context
2. Database results

Document Context:
{document_context}

Database Result:
{database_context}

Question:
{question}

Answer:
"""