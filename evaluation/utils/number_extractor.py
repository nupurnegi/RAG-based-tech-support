import re

def extract_score(response: str) -> float:
    match = re.search(r"[-+]?\d*\.?\d+", response)
    if not match:
        raise ValueError(f"No numeric score found in response:\n{response}")
    return float(match.group())
