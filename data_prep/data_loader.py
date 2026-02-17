"""
Data loading and preprocessing module for Ubuntu dialogue dataset.

This module handles:
- Loading Ubuntu dialogue QA dataset from HuggingFace
- Text cleaning and normalization
- Dataset preprocessing for embedding generation
"""

import os
import sys
import re
from datasets import load_dataset

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import HF_TOKEN


def load_ubuntu_dataset():
    """
    Load the Ubuntu dialogue QA dataset from HuggingFace.
    
    Returns:
        Dataset: HuggingFace dataset object containing Ubuntu support conversations
    """
    # Authenticate with HuggingFace
    os.system(f"hf auth login --token {HF_TOKEN}")
    
    # Load the dataset
    dataset = load_dataset("sedthh/ubuntu_dialogue_qa", split="train")
    
    return dataset


def clean_text(text):
    """
    Clean and normalize text by removing URLs, special characters, and extra whitespace.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned and normalized text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    
    # Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()


def preprocess_dataset(dataset):
    """
    Preprocess the Ubuntu dataset by cleaning questions and answers.
    
    Args:
        dataset: HuggingFace dataset object
        
    Returns:
        tuple: (questions, answers) - Lists of cleaned questions and answers
    """
    questions = []
    answers = []

    for row in dataset:
        # Clean question and answer
        question = clean_text(row["INSTRUCTION"])
        answer = clean_text(row["RESPONSE"])
        
        # Only include non-empty pairs
        if question and answer:
            questions.append(question)
            answers.append(answer)

    return questions, answers
