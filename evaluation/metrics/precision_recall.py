from evaluation.utils.claim_extractor import extract_claims
from evaluation.utils.llm_judge import judge_with_llm

def precision_recall(context, answer):
    claims = extract_claims(answer)

    if not claims:
        return 0.0, 0.0

    relevant = 0

    for claim in claims:
        prompt = f"""
        Context:
        {context}

        Claim:
        {claim}

        Is this claim relevant and correct?
        YES or NO.
        """
        if judge_with_llm(prompt).startswith("YES"):
            relevant += 1
        print("relevant:", relevant)
    precision = relevant / len(claims)
    print("precision:",precision)
    
    recall_prompt = f"""    
    Context:
    {context}

    Answer:
    {answer}

    Rate recall from 0 to 1 (how much important information was covered).
    0 = not at all
    1 = perfectly

    Output ONLY a number.
    """
    recall = judge_with_llm(recall_prompt).strip().split()[0]
    print("recall: ", recall)
    return precision, recall
