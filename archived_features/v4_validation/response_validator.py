"""
Response validation module to reduce hallucination.

This module:
- Validates responses against retrieved context
- Checks if claims are supported by context using semantic similarity
- Filters out hallucinated content
"""

import re
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize sentence transformer model (lightweight, fast)
_model = None

def get_sentence_model():
    """Lazy load sentence transformer model."""
    global _model
    if _model is None:
        print("Loading sentence transformer model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded!")
    return _model


def extract_claims(text: str) -> List[str]:
    """
    Extract individual claims/statements from text.
    
    Args:
        text (str): Response text to extract claims from
        
    Returns:
        List[str]: List of individual claims
    """
    # Split by sentences
    sentences = re.split(r'[.!?]+', text)
    
    # Clean and filter
    claims = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10:  # Ignore very short fragments
            claims.append(sentence)
    
    return claims


def is_claim_supported(claim: str, context: str, threshold: float = 0.65) -> bool:
    """
    Check if a claim is supported by the context using semantic similarity.
    
    Uses sentence embeddings to check if the claim's meaning is similar
    to any part of the context, catching paraphrasing and synonyms.
    
    Args:
        claim (str): Individual claim to validate
        context (str): Retrieved context
        threshold (float): Minimum similarity score (default: 0.65)
        
    Returns:
        bool: True if claim appears supported by context
    """
    # Handle empty inputs
    if not claim or not claim.strip():
        return True
    
    if not context or not context.strip():
        return False
    
    try:
        # Get sentence transformer model
        model = get_sentence_model()
        
        # Split context into sentences for comparison
        context_sentences = [s.strip() for s in re.split(r'[.!?\n]+', context) if s.strip()]
        
        if not context_sentences:
            return False
        
        # Get embeddings
        claim_embedding = model.encode([claim])
        context_embeddings = model.encode(context_sentences)
        
        # Calculate cosine similarity between claim and each context sentence
        similarities = cosine_similarity(claim_embedding, context_embeddings)[0]
        
        # Check if any context sentence is similar enough
        max_similarity = np.max(similarities)
        
        # Debug logging
        if max_similarity < threshold:
            print(f"  [Validation] Claim not supported: {claim[:60]}... (max sim: {max_similarity:.2f})")
        
        return max_similarity >= threshold
        
    except Exception as e:
        print(f"  [Validation] Error in semantic validation: {e}")
        # Fallback to simple keyword matching if semantic fails
        claim_lower = claim.lower()
        context_lower = context.lower()
        
        # Extract key words
        claim_words = set(re.findall(r'\b\w{4,}\b', claim_lower))  # Words with 4+ chars
        if not claim_words:
            return True
        
        matches = sum(1 for word in claim_words if word in context_lower)
        return (matches / len(claim_words)) >= 0.4


def calculate_support_score(answer: str, context: str) -> float:
    """
    Calculate what percentage of claims in answer are supported by context.
    
    Args:
        answer (str): Generated answer
        context (str): Retrieved context
        
    Returns:
        float: Support score between 0 and 1
    """
    claims = extract_claims(answer)
    
    if not claims:
        return 1.0  # No claims to validate
    
    supported_count = sum(1 for claim in claims if is_claim_supported(claim, context))
    return supported_count / len(claims)


def validate_response(answer: str, context: str, threshold: float = 0.5) -> Tuple[bool, float, str]:
    """
    Validate if response is sufficiently grounded in context using semantic similarity.
    
    Args:
        answer (str): Generated answer to validate
        context (str): Retrieved context
        threshold (float): Minimum support score required (default: 0.5)
        
    Returns:
        Tuple[bool, float, str]: (is_valid, support_score, validated_answer)
            - is_valid: Whether answer passes validation
            - support_score: Percentage of claims supported (0-1)
            - validated_answer: Original answer or fallback message
    """
    # Calculate support score using semantic similarity
    support_score = calculate_support_score(answer, context)
    
    print(f"  [Validation] Support score: {support_score:.2f}, Threshold: {threshold:.2f}")
    
    # Check if answer meets threshold
    is_valid = support_score >= threshold
    
    if is_valid:
        print(f"  [Validation] ✓ Response PASSED validation")
        return True, support_score, answer
    else:
        print(f"  [Validation] ✗ Response FAILED validation - using fallback")
        # Return fallback message
        fallback = ("I don't have enough specific information in my knowledge base to fully answer this question. "
                   "Could you provide more details or rephrase your question?")
        return False, support_score, fallback


def filter_unsupported_claims(answer: str, context: str) -> str:
    """
    Filter out unsupported claims from answer, keeping only grounded content.
    
    Args:
        answer (str): Generated answer
        context (str): Retrieved context
        
    Returns:
        str: Filtered answer with only supported claims
    """
    claims = extract_claims(answer)
    
    if not claims:
        return answer
    
    # Keep only supported claims
    supported_claims = [
        claim for claim in claims 
        if is_claim_supported(claim, context)
    ]
    
    if not supported_claims:
        return ("I don't have enough specific information in my knowledge base to answer this question. "
               "Could you provide more details?")
    
    # Reconstruct answer from supported claims
    filtered_answer = ". ".join(supported_claims) + "."
    
    return filtered_answer


def enhance_with_context_check(answer: str, context: str) -> str:
    """
    Enhance answer by adding context availability check.
    
    If answer seems to go beyond context, add disclaimer.
    
    Args:
        answer (str): Generated answer
        context (str): Retrieved context
        
    Returns:
        str: Enhanced answer with disclaimer if needed
    """
    support_score = calculate_support_score(answer, context)
    
    if support_score < 0.8:
        disclaimer = ("\n\nNote: Some of this information may be general guidance. "
                     "For your specific situation, please verify these steps apply to your Ubuntu version.")
        return answer + disclaimer
    
    return answer

 
