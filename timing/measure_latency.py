"""
Latency measurement script for RAG system.

This script measures the actual response time for each component:
- Intent Analysis
- Vector Retrieval
- Response Generation
- Total end-to-end time

Run this to get accurate latency metrics for your dissertation.
"""

import os
import sys
import time
import asyncio

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from context_expansion.intent_analyzer import analyze_intent
from retriever.retriever import retrieve_context
from retriever.vector_store import get_vectorstore
from generator.generator_llm import generator_llm
from generator.prompt_builder import build_prompt


def measure_intent_analysis(query):
    """Measure intent analysis latency."""
    print(f"\n{'='*80}")
    print("MEASURING INTENT ANALYSIS")
    print(f"{'='*80}")
    print(f"Query: {query}")
    
    start = time.time()
    intent = analyze_intent(query)
    elapsed = time.time() - start
    
    print(f"Status: {intent['status']}")
    print(f"⏱️  Time: {elapsed:.3f} seconds")
    
    return elapsed, intent


def measure_retrieval(query, vectorstore):
    """Measure retrieval latency."""
    print(f"\n{'='*80}")
    print("MEASURING VECTOR RETRIEVAL")
    print(f"{'='*80}")
    
    start = time.time()
    context, similarity_score = retrieve_context(vectorstore, query)
    elapsed = time.time() - start
    
    print(f"Similarity Score: {similarity_score:.4f}")
    print(f"Context Length: {len(context)} characters")
    print(f"⏱️  Time: {elapsed:.3f} seconds")
    
    return elapsed, context, similarity_score


def measure_generation(query, context, history=[]):
    """Measure response generation latency."""
    print(f"\n{'='*80}")
    print("MEASURING RESPONSE GENERATION")
    print(f"{'='*80}")
    
    # Build prompt
    prompt = build_prompt(
        user_question=query,
        context=context,
        history=history
    )
    
    start = time.time()
    response = generator_llm().generate_text(prompt)
    elapsed = time.time() - start
    
    print(f"Response Length: {len(response)} characters")
    print(f"⏱️  Time: {elapsed:.3f} seconds")
    
    return elapsed, response


def measure_end_to_end(query, vectorstore=None):
    """Measure complete end-to-end latency."""
    print(f"\n{'='*80}")
    print("MEASURING END-TO-END LATENCY")
    print(f"{'='*80}")
    print(f"Query: {query}")
    
    total_start = time.time()
    
    # 1. Intent Analysis
    intent_start = time.time()
    intent = analyze_intent(query)
    intent_time = time.time() - intent_start
    
    if intent["status"] == "AMBIGUOUS":
        total_time = time.time() - total_start
        print(f"\n⚠️  Query marked as AMBIGUOUS - NO RETRIEVAL PERFORMED")
        print(f"📊 BREAKDOWN:")
        print(f"  Intent Analysis:     {intent_time:.3f}s (100%)")
        print(f"  Vector Retrieval:    0.000s (skipped)")
        print(f"  Response Generation: 0.000s (skipped)")
        print(f"  ─────────────────────────────")
        print(f"  ⏱️  TOTAL:            {total_time:.3f}s")
        return {
            "query": query,
            "status": "AMBIGUOUS",
            "intent_time": intent_time,
            "retrieval_time": 0.0,
            "generation_time": 0.0,
            "total_time": total_time
        }
    
    # 2. Retrieval (only for CLEAR queries)
    retrieval_start = time.time()
    if vectorstore is None:
        vectorstore = get_vectorstore()
    context, similarity_score = retrieve_context(vectorstore, query)
    retrieval_time = time.time() - retrieval_start
    
    # 3. Generation
    generation_start = time.time()
    prompt = build_prompt(user_question=query, context=context, history=[])
    response = generator_llm().generate_text(prompt)
    generation_time = time.time() - generation_start
    
    total_time = time.time() - total_start
    
    print(f"\n📊 BREAKDOWN:")
    print(f"  Intent Analysis:     {intent_time:.3f}s ({intent_time/total_time*100:.1f}%)")
    print(f"  Vector Retrieval:    {retrieval_time:.3f}s ({retrieval_time/total_time*100:.1f}%)")
    print(f"  Response Generation: {generation_time:.3f}s ({generation_time/total_time*100:.1f}%)")
    print(f"  ─────────────────────────────")
    print(f"  ⏱️  TOTAL:            {total_time:.3f}s")
    
    return {
        "query": query,
        "status": "CLEAR",
        "intent_time": intent_time,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": total_time,
        "similarity_score": similarity_score,
        "response_length": len(response)
    }


def run_multiple_measurements(queries):
    """Run measurements on multiple queries and calculate averages."""
    print(f"\n{'='*80}")
    print("RUNNING MULTIPLE MEASUREMENTS")
    print(f"{'='*80}")
    
    # Initialize vectorstore ONCE (this is the slow part - ~13 seconds)
    print("\n⏳ Initializing vector store (loading embedding model + connecting to Milvus)...")
    init_start = time.time()
    vectorstore = get_vectorstore()
    init_time = time.time() - init_start
    print(f"✅ Vector store initialized in {init_time:.3f} seconds")
    print(f"   (This happens once at startup, not per query)")
    
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n\n{'#'*80}")
        print(f"# QUERY {i}/{len(queries)}")
        print(f"{'#'*80}")
        
        # Pass vectorstore to avoid re-initialization
        result = measure_end_to_end(query, vectorstore)
        results.append(result)
        
        # Small delay between queries
        time.sleep(1)
    
    # Calculate averages for CLEAR queries only
    clear_results = [r for r in results if r["status"] == "CLEAR"]
    
    if clear_results:
        avg_intent = sum(r["intent_time"] for r in clear_results) / len(clear_results)
        avg_retrieval = sum(r["retrieval_time"] for r in clear_results) / len(clear_results)
        avg_generation = sum(r["generation_time"] for r in clear_results) / len(clear_results)
        avg_total = sum(r["total_time"] for r in clear_results) / len(clear_results)
        
        print(f"\n\n{'='*80}")
        print("AVERAGE LATENCY (CLEAR QUERIES ONLY)")
        print(f"{'='*80}")
        print(f"Intent Analysis:     {avg_intent:.3f}s")
        print(f"Vector Retrieval:    {avg_retrieval:.3f}s")
        print(f"Response Generation: {avg_generation:.3f}s")
        print(f"─────────────────────────────")
        print(f"⏱️  TOTAL:            {avg_total:.3f}s")
        print(f"\nBased on {len(clear_results)} CLEAR queries")
    
    return results


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    RAG SYSTEM LATENCY MEASUREMENT                          ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Test queries - mix of simple and complex
    test_queries = [
        "How do I fix broken packages?",
        "My system is broke."
    ]
    
    print("This script will measure latency for each component:")
    print("  1. Intent Analysis")
    print("  2. Vector Retrieval")
    print("  3. Response Generation")
    print("  4. Total End-to-End Time")
    print(f"\nTesting with {len(test_queries)} queries...")
    
    input("\nPress Enter to start measurements...")
    
    # Run measurements
    results = run_multiple_measurements(test_queries)
    
    print(f"\n\n{'='*80}")
    print("MEASUREMENT COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved in memory. You can now update ARCHITECTURE_DIAGRAM.md")
    print(f"with the actual measured values.")
    print(f"\n✅ Done!")

 
