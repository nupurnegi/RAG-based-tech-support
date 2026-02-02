from evaluation.utils.claim_extractor import extract_claims
from evaluation.utils.llm_judge import judge_with_llm
from evaluation.utils.number_extractor import extract_score

def faithfulness(context, answer):
    claims = extract_claims(answer)

    supported = 0

    for claim in claims:
        prompt = f"""
        You are a LLM performance Judge for faithfulness.

        Context:
        {context}

        Claim:
        {claim}

        Evaluate whether the claims are supported ONLY by the context. 
        Do not provide the Explanation in the output.

        Give ONLY a number between 0 and 1:
        1 = All claims are supported by the context
        0 = Answer contains hallucinated or unsupported claims        
        """
        verdict = judge_with_llm(prompt)
        print("verdict:", verdict)
        # if verdict.strip().upper().startswith("YES"):
        #     supported += 1

    if not claims:
        return 1.0
    print("verdict:", verdict)
    return extract_score(verdict)/len(claims)