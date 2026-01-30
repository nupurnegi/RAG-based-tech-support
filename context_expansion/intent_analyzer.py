import json
from context_expansion.intent_prompt import build_intent_prompt
from context_expansion.intent_llm import intent_llm

def extract_first_json(text: str):
    stack = []
    start = None

    for i, ch in enumerate(text):
        if ch == "{":
            if not stack:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    return text[start:i+1]

    return None

def analyze_intent(user_query):
    prompt = build_intent_prompt(user_query)
    # response = load_llm().generate_text(prompt)
    response = intent_llm().generate_text(prompt).strip()
    json_block = extract_first_json(response)
    print(json_block)
    
    if json_block:
        try:
            return json.loads(json_block)
        except json.JSONDecodeError:
            pass
