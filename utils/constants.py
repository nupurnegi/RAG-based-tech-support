"""
Constants used across the RAG application.

This module centralizes all magic numbers and configuration constants
that are used in multiple places throughout the application.
"""

# ============================================================================
# RETRIEVAL CONSTANTS
# ============================================================================
DEFAULT_RETRIEVAL_K = 8                    # Initial number of documents to retrieve
EXPANDED_RETRIEVAL_K = 12                  # Expanded search when few results found
HIGH_SIMILARITY_THRESHOLD = 0.5            # Primary similarity threshold
LOW_SIMILARITY_THRESHOLD = 0.4             # Fallback similarity threshold
MIN_RELEVANT_DOCS = 3                      # Minimum documents needed before expansion

# ============================================================================
# GENERATION CONSTANTS
# ============================================================================
STREAMING_DELAY_SECONDS = 0.005            # Delay between tokens for streaming effect (reduced for faster display)
MAX_CONVERSATION_HISTORY_TURNS = 3         # Number of recent conversation turns to include

# ============================================================================
# UI CONSTANTS
# ============================================================================
CHATBOT_HEIGHT = 800                       # Height of chat window in pixels
TEXTBOX_INITIAL_LINES = 2                  # Initial height of input textbox
TEXTBOX_MAX_LINES = 5                      # Maximum height of input textbox
SERVER_PORT = 7860                         # Default Gradio server port

# ============================================================================
# LOGGING CONSTANTS
# ============================================================================
LOG_SEPARATOR = "=" * 80                   # Separator line for console logs
CONTEXT_PREVIEW_LENGTH = 500               # Characters to show in context preview

 
