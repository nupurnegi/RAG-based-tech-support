"""
Context retrieval module for RAG system.

This module handles:
- Semantic search in vector database
- Document filtering by relevance
- Context formatting for LLM
"""


def retrieve_context(vectorstore, query, k=8):
    """
    Retrieve relevant context from vector store for a given query.
    
    This function performs semantic search, filters results by similarity score,
    and formats the retrieved documents as context for the LLM.
    
    Args:
        vectorstore: Milvus vector store instance
        query (str): User's question
        k (int): Number of documents to retrieve initially (default: 8)
        
    Returns:
        tuple: (context, highest_score)
            - context (str): Formatted context string with Q&A pairs
            - highest_score (float): Highest similarity score among retrieved docs
    """
    # Initial retrieval with similarity scores
    docs_with_scores = vectorstore.similarity_search_with_score(query, k=k)
    
    # Filter documents by similarity threshold (balanced for quality and coverage)
    relevant_docs = [(d, score) for d, score in docs_with_scores if score > 0.5]
    
    # If too few relevant docs found, expand search with lower threshold
    if len(relevant_docs) < 3:
        docs_with_scores = vectorstore.similarity_search_with_score(query, k=12)
        relevant_docs = [(d, score) for d, score in docs_with_scores if score > 0.4]
    
    # Build context string from relevant documents
    context = ""
    highest_score = 0.0
    
    for doc, score in relevant_docs:
        # Track highest similarity score
        if score > highest_score:
            highest_score = score
        
        # Extract answer from metadata
        answer = doc.metadata.get("answer", "")
        
        # Format as Q&A pair
        context += f"User: {doc.page_content}\nAssistant: {answer}\n\n"
    
    # Log retrieval statistics
    print(f"retrieve_context: Retrieved {len(relevant_docs)} docs, highest score: {highest_score:.4f}")
    
    return context.strip(), highest_score
