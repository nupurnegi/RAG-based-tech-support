def retrieve_context(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=4)

    context = ""
    for d in docs:
        answer = d.metadata.get("answer", "")
        context += f"User: {d.page_content}\Assistant: {answer}\n\n"

    return context.strip()
