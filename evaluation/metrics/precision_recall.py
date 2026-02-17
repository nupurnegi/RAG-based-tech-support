"""
Precision and Recall metrics for evaluating answer quality.

Precision: How many claims in the answer are correct
Recall: How much important information from context is covered
"""

from evaluation.utils.claim_extractor import extract_claims
from evaluation.utils.llm_judge import judge_with_llm
from evaluation.utils.number_extractor import extract_score


def precision_recall(context, answer):
    """
    Calculate precision and recall scores.
    
    Args:
        context (str): Retrieved context
        answer (str): Generated answer
        
    Returns:
        tuple: (precision, recall) both as floats between 0 and 1
    """
    claims = extract_claims(answer)

    if not claims:
        return 0.0, 0.0

    relevant = 0

    for i, claim in enumerate(claims, 1):
        prompt = f"""
        Context:
        {context}

        Claim:
        {claim}

        Is this claim relevant and correct based on the context?
        Answer with YES or NO only.
        """
        verdict = judge_with_llm(prompt).strip().upper()
        if verdict.startswith("YES"):
            relevant += 1
        print(f"Claim {i}/{len(claims)} - Relevant: {verdict.startswith('YES')}")
    
    precision = relevant / len(claims)
    print(f"Precision: {precision:.2f}")
    
    # Calculate recall
    recall_prompt = f"""
    Context:
    {context}

    Answer:
    {answer}

    Rate recall from 0 to 1 (how much important information from context was covered in the answer).
    0 = not at all
    1 = perfectly

    Output ONLY a number between 0 and 1.
    """
    recall_response = judge_with_llm(recall_prompt)
    recall = extract_score(recall_response)
    print(f"Recall: {recall:.2f}")
    
    return precision, recall
