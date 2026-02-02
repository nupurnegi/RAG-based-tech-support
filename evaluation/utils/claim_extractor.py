def extract_claims(answer):
    # Simple baseline: split by sentences
    claims = [c.strip() for c in answer.split(".") if len(c.strip()) > 10]
    return claims
