"""
Faithfulness metric for evaluating if generated answers are grounded in context.

This metric checks if all claims in the answer are supported by the retrieved context.
"""

from evaluation.utils.claim_extractor import extract_claims
from evaluation.utils.llm_judge import judge_with_llm
from evaluation.utils.number_extractor import extract_score


def faithfulness(context, answer):
    """
    Calculate faithfulness score by checking if answer claims are supported by context.
    
    Args:
        context (str): Retrieved context
        answer (str): Generated answer
        
    Returns:
        float: Faithfulness score between 0 and 1
    """
    claims = extract_claims(answer)
    
    # If no claims, consider it faithful (empty answer)
    if not claims:
        return 1.0

    total_score = 0.0

    for i, claim in enumerate(claims, 1):
        prompt = f"""
        You are a LLM performance Judge for faithfulness.

        Context:
        {context}

        Claim:
        {claim}

        Evaluate whether this claim is supported ONLY by the context.
        Do not provide any explanation in the output.

        Give ONLY a number between 0 and 1:
        1 = Claim is fully supported by the context
        0 = Claim is not supported or hallucinated
        """
        verdict = judge_with_llm(prompt)
        score = extract_score(verdict)
        total_score += score
        print(f"Claim {i}/{len(claims)} - verdict: {verdict.strip()} - score: {score}")

    # Calculate average faithfulness across all claims
    faithfulness_score = total_score / len(claims)
    print(f"Overall Faithfulness: {faithfulness_score:.2f}")
    return faithfulness_score