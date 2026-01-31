def build_intent_prompt(user_query):
    return f"""
    You are an INTENT CLASSIFIER for an Ubuntu technical support RAG system.

    A query status is CLEAR if it contains Ubuntu issues and thus can be used to retrieve Ubuntu troubleshooting documents.

    A query status is AMBIGUOUS only if the query does not have Ubuntu issues or it is too vague to retrieve any Ubuntu-related documents.

    IMPORTANT:
    - Generate a follow-up question ONLY if the status is AMBIGUOUS.
    - Do not generate any user queries. ONLY use the one given below query to generate the JSON as per the instructions given above. 

    Analyze the following single user query:
    <<<{user_query}>>>

    Generated response should be in below JSON format ONLY. Stop the text generation once the JSON is ready:
    {{
    "status": "CLEAR" or "AMBIGUOUS",
    "follow_up_question": ""
    }}
    """






    # You are a classifier for a technical support RAG system.

    # Definition of AMBIGUOUS:
    # A query is AMBIGUOUS ONLY if it cannot reasonably be used to search a technical support knowledge base without additional clarification.

    # User Query:
    # {user_query}

    # Mark the query as CLEAR if:
    # - It mentions a problem, symptom, or task
    # - Even if details like logs, versions, or steps are missing
    # - Even if the issue is broad

    # Mark the query as AMBIGUOUS ONLY if:
    # - No specific problem or symptom is mentioned
    # - OR multiple unrelated problems are mentioned
    # - OR the query is too vague to retrieve any relevant documents

    # IMPORTANT:
    # Default to CLEAR unless clarification is strictly required.

    # Output JSON ONLY:
    # {{
    # "status": "CLEAR" or "AMBIGUOUS",
    # "follow_up_question": ""
    # }}


### ISSUE: Marking every query as AMBIGUOUS 
# |
# |
# |
# V
# Analyze the user query below.
# If the query is ambiguous or lacks sufficient technical detail, generate a clarifying follow-up question.
# If the query is clear and specific, respond with: CLEAR 

