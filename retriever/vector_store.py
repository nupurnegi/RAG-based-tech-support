"""
Vector store initialization module for Milvus database.

This module handles:
- Connection to Milvus vector database
- Embedding function initialization
- Vector store configuration
"""

import os
import sys
import warnings
from langchain_milvus import Milvus
from langchain_huggingface import HuggingFaceEmbeddings

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import EMBEDDING_MODEL_NAME, COLLECTION_NAME, MILVUS_URL, MILVUS_TOKEN

# Suppress Milvus async warnings (async operations not needed for our synchronous use case)
warnings.filterwarnings('ignore', message='.*AsyncMilvusClient.*')
warnings.filterwarnings('ignore', message='.*async connection.*')


def get_vectorstore():
    """
    Initialize and return a Milvus vector store instance.
    
    This function creates a connection to the Milvus vector database
    with the configured embedding model and collection.
    
    Returns:
        Milvus: Configured Milvus vector store instance
    """
    # Initialize embedding function
    embedding_fn = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    # Create Milvus vector store instance
    vectorstore = Milvus(
        embedding_function=embedding_fn,
        collection_name=COLLECTION_NAME,
        connection_args={
            "uri": MILVUS_URL,
            "token": MILVUS_TOKEN
        },
        vector_field="embedding",
        text_field="question"
    )

    return vectorstore
