"""
Intent analysis module for query classification.

This module handles:
- Query intent classification (CLEAR vs AMBIGUOUS)
- JSON extraction from LLM responses
- Fallback handling for parsing errors
"""

import json
from context_expansion.intent_prompt import build_intent_prompt
from context_expansion.intent_llm import intent_llm


def extract_first_json(text):
    """
    Extract the first valid JSON object from text using bracket matching.
    
    Args:
        text (str): Text containing JSON object
        
    Returns:
        str or None: Extracted JSON string, or None if not found
    """
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
    """
    Analyze user query intent and classify as CLEAR or AMBIGUOUS.
    
    This function:
    1. Generates a classification prompt
    2. Gets LLM response
    3. Extracts and parses JSON
    4. Ensures follow_up_question is empty for CLEAR queries
    5. Falls back to CLEAR if parsing fails
    
    Args:
        user_query (str): User's input query
        
    Returns:
        dict: Classification result with keys:
            - status (str): "CLEAR" or "AMBIGUOUS"
            - follow_up_question (str): Follow-up question if AMBIGUOUS, empty if CLEAR
    """
    # Build classification prompt
    prompt = build_intent_prompt(user_query)
    
    # Get LLM response
    response = intent_llm().generate_text(prompt).strip()
    
    # Extract JSON from response
    json_block = extract_first_json(response)
    
    # Log for debugging
    print(f"Intent Analysis - Raw response: {response}")
    print(f"Intent Analysis - Extracted JSON: {json_block}")
    
    # Parse JSON if found
    if json_block:
        try:
            result = json.loads(json_block)
            
            # Ensure follow_up_question is empty for CLEAR status
            if result.get("status") == "CLEAR":
                result["follow_up_question"] = ""
            
            print(f"Intent Analysis - Final result: {result}")
            return result
            
        except json.JSONDecodeError as e:
            print(f"Intent Analysis - JSON decode error: {e}")
    
    # Fallback: Default to CLEAR for technical queries
    print("Intent Analysis - Fallback to CLEAR")
    return {"status": "CLEAR", "follow_up_question": ""}
