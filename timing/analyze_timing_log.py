"""
Analyze timing log data collected from chatbot.py

This script reads timing_log.json and provides:
- Average latency by component
- Breakdown by query status (CLEAR vs AMBIGUOUS)
- Performance statistics
- Visualization-ready data
"""

import json
import os
from datetime import datetime
from statistics import mean, median, stdev


def load_timing_log(filename="timing/timing_log.json"):
    """Load timing log from JSON file."""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        print(f"   Run chatbot.py with ENABLE_TIMING=True to generate timing data.")
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)


def analyze_timing_data(logs):
    """Analyze timing data and print statistics."""
    if not logs:
        print("No timing data available.")
        return
    
    # Separate by status
    clear_logs = [log for log in logs if log["status"] == "CLEAR"]
    ambiguous_logs = [log for log in logs if log["status"] == "AMBIGUOUS"]
    
    print(f"\n{'='*80}")
    print("TIMING LOG ANALYSIS")
    print(f"{'='*80}")
    print(f"Total Queries: {len(logs)}")
    print(f"  - CLEAR: {len(clear_logs)}")
    print(f"  - AMBIGUOUS: {len(ambiguous_logs)}")
    
    # Analyze CLEAR queries
    if clear_logs:
        print(f"\n{'='*80}")
        print("CLEAR QUERIES ANALYSIS")
        print(f"{'='*80}")
        
        intent_times = [log["intent_time"] for log in clear_logs]
        retrieval_times = [log["retrieval_time"] for log in clear_logs]
        generation_times = [log["generation_time"] for log in clear_logs]
        total_times = [log["total_time"] for log in clear_logs]
        similarity_scores = [log["similarity_score"] for log in clear_logs]
        
        print(f"\nIntent Analysis:")
        print(f"  Average: {mean(intent_times):.3f}s")
        print(f"  Median:  {median(intent_times):.3f}s")
        print(f"  Min:     {min(intent_times):.3f}s")
        print(f"  Max:     {max(intent_times):.3f}s")
        if len(intent_times) > 1:
            print(f"  StdDev:  {stdev(intent_times):.3f}s")
        
        print(f"\nVector Retrieval:")
        print(f"  Average: {mean(retrieval_times):.3f}s")
        print(f"  Median:  {median(retrieval_times):.3f}s")
        print(f"  Min:     {min(retrieval_times):.3f}s")
        print(f"  Max:     {max(retrieval_times):.3f}s")
        if len(retrieval_times) > 1:
            print(f"  StdDev:  {stdev(retrieval_times):.3f}s")
        
        print(f"\nResponse Generation:")
        print(f"  Average: {mean(generation_times):.3f}s")
        print(f"  Median:  {median(generation_times):.3f}s")
        print(f"  Min:     {min(generation_times):.3f}s")
        print(f"  Max:     {max(generation_times):.3f}s")
        if len(generation_times) > 1:
            print(f"  StdDev:  {stdev(generation_times):.3f}s")
        
        print(f"\nTotal End-to-End:")
        print(f"  Average: {mean(total_times):.3f}s")
        print(f"  Median:  {median(total_times):.3f}s")
        print(f"  Min:     {min(total_times):.3f}s")
        print(f"  Max:     {max(total_times):.3f}s")
        if len(total_times) > 1:
            print(f"  StdDev:  {stdev(total_times):.3f}s")
        
        print(f"\nSimilarity Scores:")
        print(f"  Average: {mean(similarity_scores):.4f}")
        print(f"  Median:  {median(similarity_scores):.4f}")
        print(f"  Min:     {min(similarity_scores):.4f}")
        print(f"  Max:     {max(similarity_scores):.4f}")
        
        # Percentage breakdown
        avg_total = mean(total_times)
        avg_intent = mean(intent_times)
        avg_retrieval = mean(retrieval_times)
        avg_generation = mean(generation_times)
        
        print(f"\nAverage Percentage Breakdown:")
        print(f"  Intent Analysis:     {avg_intent/avg_total*100:.1f}%")
        print(f"  Vector Retrieval:    {avg_retrieval/avg_total*100:.1f}%")
        print(f"  Response Generation: {avg_generation/avg_total*100:.1f}%")
    
    # Analyze AMBIGUOUS queries
    if ambiguous_logs:
        print(f"\n{'='*80}")
        print("AMBIGUOUS QUERIES ANALYSIS")
        print(f"{'='*80}")
        
        intent_times = [log["intent_time"] for log in ambiguous_logs]
        total_times = [log["total_time"] for log in ambiguous_logs]
        
        print(f"\nIntent Analysis (only component):")
        print(f"  Average: {mean(intent_times):.3f}s")
        print(f"  Median:  {median(intent_times):.3f}s")
        print(f"  Min:     {min(intent_times):.3f}s")
        print(f"  Max:     {max(intent_times):.3f}s")
        if len(intent_times) > 1:
            print(f"  StdDev:  {stdev(intent_times):.3f}s")
        
        print(f"\nTotal Time:")
        print(f"  Average: {mean(total_times):.3f}s")
        print(f"  Median:  {median(total_times):.3f}s")
    
    # Recent queries
    print(f"\n{'='*80}")
    print("RECENT QUERIES (Last 5)")
    print(f"{'='*80}")
    
    for i, log in enumerate(logs[-5:], 1):
        timestamp = datetime.fromisoformat(log["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{i}. [{timestamp}] {log['status']}")
        print(f"   Query: {log['query'][:60]}{'...' if len(log['query']) > 60 else ''}")
        print(f"   Total: {log['total_time']:.3f}s")
        if log['status'] == 'CLEAR':
            print(f"   Breakdown: Intent={log['intent_time']:.3f}s, "
                  f"Retrieval={log['retrieval_time']:.3f}s, "
                  f"Generation={log['generation_time']:.3f}s")
            print(f"   Similarity: {log['similarity_score']:.4f}, "
                  f"Confidence: {log['confidence_level']}")


def export_summary(logs, output_file="timing/timing_summary.txt"):
    """Export summary statistics to a text file."""
    clear_logs = [log for log in logs if log["status"] == "CLEAR"]
    
    if not clear_logs:
        print("No CLEAR queries to summarize.")
        return
    
    with open(output_file, 'w') as f:
        f.write("TIMING SUMMARY FOR DISSERTATION\n")
        f.write("="*80 + "\n\n")
        
        intent_times = [log["intent_time"] for log in clear_logs]
        retrieval_times = [log["retrieval_time"] for log in clear_logs]
        generation_times = [log["generation_time"] for log in clear_logs]
        total_times = [log["total_time"] for log in clear_logs]
        
        f.write(f"Based on {len(clear_logs)} CLEAR queries\n\n")
        
        f.write("Average Latency:\n")
        f.write(f"  Intent Analysis:     {mean(intent_times):.3f}s\n")
        f.write(f"  Vector Retrieval:    {mean(retrieval_times):.3f}s\n")
        f.write(f"  Response Generation: {mean(generation_times):.3f}s\n")
        f.write(f"  Total:               {mean(total_times):.3f}s\n\n")
        
        f.write("Latency Range:\n")
        f.write(f"  Intent Analysis:     {min(intent_times):.3f}s - {max(intent_times):.3f}s\n")
        f.write(f"  Vector Retrieval:    {min(retrieval_times):.3f}s - {max(retrieval_times):.3f}s\n")
        f.write(f"  Response Generation: {min(generation_times):.3f}s - {max(generation_times):.3f}s\n")
        f.write(f"  Total:               {min(total_times):.3f}s - {max(total_times):.3f}s\n\n")
        
        avg_total = mean(total_times)
        f.write("Percentage Breakdown:\n")
        f.write(f"  Intent Analysis:     {mean(intent_times)/avg_total*100:.1f}%\n")
        f.write(f"  Vector Retrieval:    {mean(retrieval_times)/avg_total*100:.1f}%\n")
        f.write(f"  Response Generation: {mean(generation_times)/avg_total*100:.1f}%\n")
    
    print(f"\n✅ Summary exported to {output_file}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    TIMING LOG ANALYZER                                     ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Load and analyze data
    logs = load_timing_log()
    
    if logs:
        analyze_timing_data(logs)
        
        # Export summary
        export_summary(logs)
        
        print(f"\n{'='*80}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"✅ Analyzed {len(logs)} queries")
        print(f"✅ Summary exported to timing_summary.txt")
        print(f"\nUse this data for your dissertation's performance analysis section!")
    else:
        print("\n💡 To generate timing data:")
        print("   1. Ensure ENABLE_TIMING = True in chatbot.py")
        print("   2. Run: python chatbot.py")
        print("   3. Ask several queries")
        print("   4. Run this script again: python analyze_timing_log.py")

 
