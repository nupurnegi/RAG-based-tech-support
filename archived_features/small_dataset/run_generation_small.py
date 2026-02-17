"""
Generation script for RAG system evaluation - SMALL DATASET VERSION.

This script uses only 5 queries to save tokens.

Usage:
    python evaluation/run_generation_small.py
"""

import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retriever.vector_store import get_vectorstore
from retriever.retriever import retrieve_context
from generator.prompt_builder import build_prompt
from generator.generator_llm import generator_llm
from generator.response_validator import validate_response


def run_rag(query, vectorstore):
    """
    Run the complete RAG pipeline for a single query.
    
    Args:
        query (str): User query
        vectorstore: Milvus vector store instance
        
    Returns:
        dict: Result with query, context, answer, and similarity score
    """
    # Retrieve relevant context
    context, similarity = retrieve_context(vectorstore, query)

    # Build prompt with context
    prompt = build_prompt(
        user_question=query,
        context=context,
        history=[]
    )

    # Generate answer
    answer = generator_llm().generate_text(prompt)
    
    # Validate response against context using semantic similarity
    is_valid, support_score, validated_answer = validate_response(answer, context, threshold=0.5)
    
    print(f"  Validation - Support Score: {support_score:.2f}, Valid: {is_valid}")

    return {
        "query": query,
        "context": context,
        "answer": validated_answer,  # Use validated answer
        "similarity": similarity,
        "support_score": support_score,
        "validation_passed": is_valid
    }


if __name__ == "__main__":
    # Load evaluation queries (SMALL VERSION)
    queries_file = "evaluation/data/eval_queries_small.json"
    
    if not os.path.exists(queries_file):
        print(f"ERROR: {queries_file} not found!")
        sys.exit(1)
    
    print(f"Loading queries from {queries_file}...")
    with open(queries_file) as f:
        queries = json.load(f)
    
    print(f"Found {len(queries)} queries to evaluate (SMALL DATASET)")
    
    # Initialize vector store once
    print("Initializing vector store...")
    vectorstore = get_vectorstore()
    print("Vector store ready!")

    results = []

    for i, item in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"Processing {i}/{len(queries)}: {item['id']}")
        print(f"Query: {item['query']}")
        print(f"{'='*80}")
        
        try:
            output = run_rag(item["query"], vectorstore)
            results.append({
                "id": item["id"],
                **output
            })
            print(f"✓ Generated answer ({len(output['answer'])} chars)")
            print(f"✓ Similarity score: {output['similarity']:.4f}")
            print(f"✓ Support score: {output['support_score']:.2f}")
            print(f"✓ Validation passed: {output['validation_passed']}")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            # Add error result
            results.append({
                "id": item["id"],
                "query": item["query"],
                "context": "",
                "answer": f"ERROR: {str(e)}",
                "similarity": 0.0,
                "support_score": 0.0,
                "validation_passed": False,
                "error": str(e)
            })

    # Save results
    output_file = "evaluation/results_small.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n\n{'='*80}")
    print(f"✅ Generation Complete!")
    print(f"{'='*80}")
    print(f"Saved {len(results)} results to {output_file}")
    print(f"\nNext step: Run scoring with:")
    print(f"  python evaluation/run_scoring_small.py")

