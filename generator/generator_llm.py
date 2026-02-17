"""
LLM initialization module for response generation.

This module handles:
- IBM Watsonx AI model initialization
- Model parameter configuration
- Warning suppression
"""

import os
import sys
import warnings
from ibm_watsonx_ai.foundation_models import ModelInference

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import PROJECT_ID, WATSONX_CREDENTIALS, WATSONX_MODEL_ID

# Suppress deprecation and lifecycle warnings for cleaner output
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*deprecated state.*')


def generator_llm():
    """
    Initialize and return IBM Watsonx AI model for response generation.
    
    Configured with parameters optimized for:
    - Factual, grounded responses (low temperature)
    - Complete answers (high max_tokens)
    - Focused output (controlled top_p)
    - Non-repetitive text (repetition penalty)
    
    Returns:
        ModelInference: Configured IBM Watsonx AI model instance
    """
    return ModelInference(
        model_id=WATSONX_MODEL_ID,
        credentials=WATSONX_CREDENTIALS,
        project_id=PROJECT_ID,
        params={
            "temperature": 0.1,              # Lower for more deterministic, factual responses
            "max_new_tokens": 300,           # Increased from 100 to avoid truncation
            "top_p": 0.85,                   # Slightly restricted for more focused responses
            "repetition_penalty": 1.1,       # Prevent repetitive text
            "stop_sequences": ["\n\nUser:", "Assistant:"]  # Stop at conversation boundaries
        }
    )