def build_prompt(user_question, context, history):

    recent_history = history[-3:]
    conversation_memory = ""

    for turn in recent_history:

        # Case 0: Skip streaming generators
        if hasattr(turn, "__iter__") and not isinstance(turn, (list, tuple, dict, str)):
            continue

        # Case 1: (user, assistant) as tuple
        # gradio chat format
        if isinstance(turn, (list, tuple)) and len(turn) == 2:
            user, assistant = turn
            conversation_memory += f"User: {user}\nAssistant: {assistant}\n"

            # Case 2: {"role": "...", "content": "..."}. as dict
            # watsonx chat format    
        elif isinstance(turn, dict):
            role = turn.get("role")
            content = turn.get("content")
            if role and content:
                conversation_memory += f"{role.capitalize()}: {content}\n"


    prompt = f"""
You are a tech support assistant. Use ONLY the context to help the user. Also keep track of the conversation.

Conversation History:
{conversation_memory}

Retrieved Context:
{context}

User Query:
{user_question}

Answer clearly and concisely as a tech support assistant.
"""
    return prompt.strip()
