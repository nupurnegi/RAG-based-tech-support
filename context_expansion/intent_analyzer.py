import json
from context_expansion.intent_prompt import build_intent_prompt
from context_expansion.intent_llm import intent_llm

def analyze_intent(user_query):
    prompt = build_intent_prompt(user_query)
    # response = load_llm().generate_text(prompt)
    response = intent_llm().generate_text(prompt).strip()
    json_start = response.find("{")
    json_end = response.rfind("}") + 1
    clean_json = response[json_start:json_end]
    print(response)   
    
    try:
        return json.loads(clean_json)
    except json.JSONDecodeError:
        return {"status": "CLEAR", "follow_up_question": []}