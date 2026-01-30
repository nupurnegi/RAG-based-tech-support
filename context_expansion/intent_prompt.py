def build_intent_prompt(user_query):
    return f"""
You are a technical support assistant.

Analyze the user query below.
If the query is ambiguous or lacks sufficient technical detail, generate a clarifying follow-up question.
If the query is clear and specific, respond with: CLEAR 

User Query:
{user_query}

Respond in JSON format:
{{
  "status": "CLEAR" or "AMBIGUOUS",
  "follow_up_question": ""
}}
"""
