"""
LLM initialization module for intent classification.

This module handles:
- IBM Watsonx AI model initialization for intent analysis
- Model parameter configuration optimized for JSON generation
- Warning suppression
"""

import os
import sys
import warnings
from ibm_watsonx_ai.foundation_models import ModelInference

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import PROJECT_ID, WATSONX_CREDENTIALS, WATSONX_INTENT_MODEL_ID, WATSONX_MODEL_ID

# Suppress deprecation and lifecycle warnings for cleaner output
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*deprecated state.*')


def intent_llm():
    """
    Initialize and return IBM Watsonx AI model for intent classification.
    
    Configured with parameters optimized for:
    - Structured JSON output
    - Complete responses (no truncation)
    - Diverse token selection for better classification
    
    Returns:
        ModelInference: Configured IBM Watsonx AI model instance
    """
    return ModelInference(
        model_id=WATSONX_MODEL_ID,
        credentials=WATSONX_CREDENTIALS,
        project_id=PROJECT_ID,
        params={
            "temperature": 0.1,           # Low for consistent classification
            "max_new_tokens": 150,        # Sufficient for complete JSON responses
            "top_p": 0.9,                 # Diverse token selection
            "stop_sequences": ["}"]       # Stop after JSON closes
        }
    )
