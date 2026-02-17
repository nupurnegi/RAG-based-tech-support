"""
Utility modules for the RAG-based Technical Support Assistant.

This package contains:
- constants: Application-wide constants and configuration values
- helpers: Reusable utility functions
"""

from utils.constants import (
    DEFAULT_RETRIEVAL_K,
    EXPANDED_RETRIEVAL_K,
    HIGH_SIMILARITY_THRESHOLD,
    LOW_SIMILARITY_THRESHOLD,
    MIN_RELEVANT_DOCS,
    STREAMING_DELAY_SECONDS,
    MAX_CONVERSATION_HISTORY_TURNS,
    CHATBOT_HEIGHT,
    TEXTBOX_INITIAL_LINES,
    TEXTBOX_MAX_LINES,
    SERVER_PORT,
    LOG_SEPARATOR,
    CONTEXT_PREVIEW_LENGTH,
)

from utils.helpers import (
    format_log_separator,
    truncate_text,
    validate_query,
    format_qa_pair,
)

__all__ = [
    # Constants
    'DEFAULT_RETRIEVAL_K',
    'EXPANDED_RETRIEVAL_K',
    'HIGH_SIMILARITY_THRESHOLD',
    'LOW_SIMILARITY_THRESHOLD',
    'MIN_RELEVANT_DOCS',
    'STREAMING_DELAY_SECONDS',
    'MAX_CONVERSATION_HISTORY_TURNS',
    'CHATBOT_HEIGHT',
    'TEXTBOX_INITIAL_LINES',
    'TEXTBOX_MAX_LINES',
    'SERVER_PORT',
    'LOG_SEPARATOR',
    'CONTEXT_PREVIEW_LENGTH',
    # Helpers
    'format_log_separator',
    'truncate_text',
    'validate_query',
    'format_qa_pair',
]

 
