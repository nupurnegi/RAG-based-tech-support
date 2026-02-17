"""
Helper utility functions used across the RAG application.

This module contains reusable utility functions that don't fit
into specific domain modules.
"""


def format_log_separator(title=""):
    """
    Create a formatted log separator with optional title.
    
    Args:
        title (str): Optional title to display in separator
        
    Returns:
        str: Formatted separator string
    """
    separator = "=" * 80
    if title:
        return f"\n{separator}\n{title}\n{separator}"
    return f"\n{separator}"


def truncate_text(text, max_length=500, suffix="..."):
    """
    Truncate text to specified length with suffix.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length before truncation
        suffix (str): Suffix to add when truncated
        
    Returns:
        str: Truncated text with suffix if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def validate_query(query):
    """
    Validate user query is not empty or whitespace only.
    
    Args:
        query (str): User query to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return bool(query and query.strip())


def format_qa_pair(question, answer):
    """
    Format a question-answer pair for context display.
    
    Args:
        question (str): Question text
        answer (str): Answer text
        
    Returns:
        str: Formatted Q&A pair
    """
    return f"User: {question}\nAssistant: {answer}\n\n"

 
