"""
Prompt building module for LLM generation.

This module handles:
- Conversation history formatting
- Context integration
- Prompt template construction
"""


def _format_conversation_history(history, max_turns=3):
    """
    Format conversation history from various input formats.
    
    Supports both Gradio format (tuples) and Watsonx format (dicts).
    
    Args:
        history (list): List of conversation turns
        max_turns (int): Maximum number of recent turns to include
        
    Returns:
        str: Formatted conversation history string
    """
    recent_history = history[-max_turns:] if history else []
    conversation_memory = ""

    for turn in recent_history:
        # Skip streaming generators
        if hasattr(turn, "__iter__") and not isinstance(turn, (list, tuple, dict, str)):
            continue

        # Handle Gradio format: (user_message, assistant_message)
        if isinstance(turn, (list, tuple)) and len(turn) == 2:
            user_msg, assistant_msg = turn
            conversation_memory += f"User: {user_msg}\nAssistant: {assistant_msg}\n"

        # Handle Watsonx format: {"role": "...", "content": "..."}
        elif isinstance(turn, dict):
            role = turn.get("role")
            content = turn.get("content")
            if role and content:
                conversation_memory += f"{role.capitalize()}: {content}\n"

    return conversation_memory


def build_prompt(user_question, context, history):
    """
    Build a complete prompt for the LLM with context and conversation history.
    
    This function creates a structured prompt that:
    - Enforces context-grounded responses
    - Includes conversation history
    - Provides clear instructions to prevent hallucination
    
    Args:
        user_question (str): Current user query
        context (str): Retrieved context from vector store
        history (list): Conversation history
        
    Returns:
        str: Complete formatted prompt for LLM
    """
    # Format conversation history
    conversation_memory = _format_conversation_history(history, max_turns=3)

    # Build structured prompt with enhanced anti-hallucination instructions
    prompt = f"""You are a technical support assistant for Ubuntu systems.

⚠️ CRITICAL RULES - VIOLATION WILL RESULT IN INCORRECT RESPONSE:

1. ONLY use information explicitly stated in the "Retrieved Context" below
2. If information is NOT in the context, you MUST say: "I don't have specific information about that in my knowledge base."
3. DO NOT use your general knowledge about Ubuntu, Linux, or computers
4. DO NOT make up or infer: commands, file paths, package names, configuration steps, or solutions
5. DO NOT provide generic advice - ONLY use exact information from the context
6. When providing solutions, directly quote or closely paraphrase the context
7. If context is incomplete, acknowledge what's missing rather than filling gaps with assumptions

VERIFICATION CHECKLIST (Check before responding):
☐ Every statement in my answer comes from the Retrieved Context
☐ I have not added any information from my general knowledge
☐ I have not made assumptions about missing details
☐ If context is insufficient, I have said "I don't have enough information"

Conversation History:
{conversation_memory}

Retrieved Context (YOUR ONLY SOURCE - DO NOT GO BEYOND THIS):
{context}

User Query:
{user_question}

Response Guidelines:
- Context has relevant info → Provide answer using ONLY that context
- Context partially relevant → Use only what's there, state what's missing
- Context not relevant → Say "I don't have specific information about that"
- NEVER fabricate technical details

Answer (based ONLY on Retrieved Context):"""
    
    # Log context preview for debugging
    print("\n" + "="*80)
    print("RETRIEVED CONTEXT:")
    print("="*80)
    context_preview = context[:500] + "..." if len(context) > 500 else context
    print(context_preview)
    print("="*80 + "\n")
    
    return prompt.strip()