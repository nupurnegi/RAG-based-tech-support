def retrieve_context(vectorstore, query):
    # docs = vectorstore.similarity_search(query, k=4)
    docs_with_scores = vectorstore.similarity_search_with_score(query, k=4)
    # Use similarity score as ambiguity signal

    context = ""
    highest_score = 0

    for d, score in docs_with_scores:
        
        # Finding highest score
        if score > highest_score:
            highest_score = score

        answer = d.metadata.get("answer", "")
        context += f"User: {d.page_content}\Assistant: {answer}\n\n"
    print("retrieve_context")
    return context.strip(), highest_score