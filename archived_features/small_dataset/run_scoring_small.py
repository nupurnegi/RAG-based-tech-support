"""
Scoring script for RAG system evaluation - SMALL DATASET VERSION.

This script scores results from the small dataset (5 queries).

Usage:
    python evaluation/run_scoring_small.py
"""

import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics.context_relevance import context_relevance
from metrics.faithfulness import faithfulness
from metrics.answer_relevance import answer_relevance
from metrics.precision_recall import precision_recall
from utils.number_extractor import extract_score


def score_single_result(item):
    """
    Score a single result with all metrics.
    
    Args:
        item (dict): Result item with query, context, answer
        
    Returns:
        dict: Item with added metrics
    """
    print(f"\n{'='*80}")
    print(f"Scoring: {item['id']}")
    print(f"{'='*80}")
    
    query = item["query"]
    context = item["context"]
    answer = item["answer"]

    metrics = {}
    
    try:
        # Context Relevance
        print("\n[1/5] Running context_relevance...")
        cr_response = context_relevance(query, context)
        metrics["context_relevance"] = extract_score(cr_response)
        
        # Faithfulness
        print("\n[2/5] Running faithfulness...")
        metrics["faithfulness"] = faithfulness(context, answer)
        
        # Hallucination Rate (inverse of faithfulness)
        metrics["hallucination_rate"] = 1 - metrics["faithfulness"]
        
        # Answer Relevance
        print("\n[3/5] Running answer_relevance...")
        ar_response = answer_relevance(query, answer)
        metrics["answer_relevance"] = extract_score(ar_response)
        
        # Precision & Recall
        print("\n[4/5] Running precision & recall...")
        precision, recall = precision_recall(context, answer)
        metrics["precision"] = precision
        metrics["recall"] = recall
        
        print(f"\n[5/5] Metrics Summary:")
        print(f"  Context Relevance: {metrics['context_relevance']:.2f}")
        print(f"  Faithfulness: {metrics['faithfulness']:.2f}")
        print(f"  Hallucination Rate: {metrics['hallucination_rate']:.2f}")
        print(f"  Answer Relevance: {metrics['answer_relevance']:.2f}")
        print(f"  Precision: {metrics['precision']:.2f}")
        print(f"  Recall: {metrics['recall']:.2f}")
        
    except Exception as e:
        print(f"ERROR scoring {item['id']}: {e}")
        # Set default values on error
        metrics = {
            "context_relevance": 0.0,
            "faithfulness": 0.0,
            "hallucination_rate": 1.0,
            "answer_relevance": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "error": str(e)
        }

    return {
        **item,
        "metrics": metrics
    }


if __name__ == "__main__":
    # Load results - handle both running from root and from evaluation directory
    if os.path.exists("evaluation/results_small.json"):
        results_file = "evaluation/results_small.json"
        output_file = "evaluation/scored_results_small.json"
    elif os.path.exists("results_small.json"):
        results_file = "results_small.json"
        output_file = "scored_results_small.json"
    else:
        print(f"ERROR: results_small.json not found!")
        print("Please run 'python evaluation/run_generation_small.py' first.")
        sys.exit(1)
    
    print(f"Loading results from {results_file}...")
    with open(results_file) as f:
        results = json.load(f)
    
    print(f"Found {len(results)} results to score (SMALL DATASET)")

    scored_results = []

    for i, item in enumerate(results, 1):
        print(f"\n\n{'#'*80}")
        print(f"# Processing {i}/{len(results)}")
        print(f"{'#'*80}")
        
        scored_item = score_single_result(item)
        scored_results.append(scored_item)

    # Save scored results
    with open(output_file, "w") as f:
        json.dump(scored_results, f, indent=2)

    print(f"\n\n{'='*80}")
    print(f"✅ Scoring Complete!")
    print(f"{'='*80}")
    print(f"Saved {len(scored_results)} scored results to {output_file}")
    
    # Calculate and display average metrics
    print(f"\n{'='*80}")
    print("AVERAGE METRICS ACROSS ALL QUERIES:")
    print(f"{'='*80}")
    
    avg_metrics = {}
    metric_names = ["context_relevance", "faithfulness", "hallucination_rate",
                    "answer_relevance", "precision", "recall"]
    
    for metric in metric_names:
        values = [r["metrics"][metric] for r in scored_results if metric in r["metrics"]]
        if values:
            avg_metrics[metric] = sum(values) / len(values)
            print(f"{metric.replace('_', ' ').title()}: {avg_metrics[metric]:.3f}")

# Made with Bob
