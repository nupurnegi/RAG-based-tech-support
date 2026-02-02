from evaluation.utils.llm_judge import judge_with_llm

def context_relevance(query, context):
    prompt = f"""
    You are a LLM performance Judge to check context relevance.

    Rate how relevant the given context is to the user query.

    Give score from 0.0 to 1.0:
    - 1.0 = fully relevant
    - 0.0 = not relevant at all

    IMPORTANT:
    Return ONLY the numeric score.
    No explanation required.
    No text generation.

    Query:
    {query}

    Context:
    {context}

    Score:
    """

    score = judge_with_llm(prompt)
    print("Context Relevance: ", score)
    return score
