def build_context(results: list[dict]) -> str:
    context_parts = []

    for result in results:
        context_parts.append(result["text"])

    return "\n\n".join(context_parts)


def build_rag_prompt(question: str, context: str) -> str:

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using only the information provided in the context.

Do not invent or assume any information that is not present in the context.

If the context does not contain enough information to answer the question, clearly say that the available documents do not contain enough information.

Keep the answer relevant and concise.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt



def build_sources(results: list[dict]) -> list[dict]:
    sources = []

    for result in results:
        sources.append({
            "document": result["document_name"],
            "chunk_id": result["chunk_id"]
        })

    return sources