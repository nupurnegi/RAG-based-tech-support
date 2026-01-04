def build_prompt(user_question, context, history):

    recent_history = history[-3:]
    conversation_memory = ""

    for turn in recent_history:
        # Case 1: (user, assistant)
        if isinstance(turn, (list, tuple)) and len(turn) == 2:
            user, assistant = turn
            conversation_memory += f"User: {user}\nAssistant: {assistant}\n"

        # Case 2: {"role": "...", "content": "..."}
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
