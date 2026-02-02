from evaluation.utils.llm_judge import judge_with_llm

def answer_relevance(query, answer):
    prompt = f"""
    User Query:
    {query}

    Generated Answer:
    {answer}

    Rate how well the Generated answer addresses the user query:
    0 = not at all
    1 = perfectly

    Output ONLY a number.
    """
    return judge_with_llm(prompt)
