# RAG System Evaluation Guide

## Overview
This evaluation framework measures the performance of your RAG system across multiple metrics.

## Metrics Evaluated

### 1. **Context Relevance** (0-1)
- Measures how relevant the retrieved context is to the user query
- Higher is better
- Target: > 0.7

### 2. **Faithfulness** (0-1)
- Measures if the answer is grounded in the retrieved context
- Checks if all claims in the answer are supported by context
- Higher is better
- Target: > 0.8

### 3. **Hallucination Rate** (0-1)
- Inverse of faithfulness (1 - faithfulness)
- Measures how much the model fabricates information
- Lower is better
- Target: < 0.2

### 4. **Answer Relevance** (0-1)
- Measures how well the answer addresses the user query
- Higher is better
- Target: > 0.85

### 5. **Precision** (0-1)
- Measures what fraction of claims in the answer are correct
- Higher is better
- Target: > 0.8

### 6. **Recall** (0-1)
- Measures how much important information from context is covered
- Higher is better
- Target: > 0.6

## How to Run Evaluation

### Step 1: Generate Responses
```bash
python evaluation/run_generation.py
```

This will:
- Load queries from `evaluation/data/eval_queries.json`
- Run RAG pipeline for each query
- Save results to `evaluation/results.json`

**Output:** `evaluation/results.json` with queries, contexts, and generated answers

### Step 2: Score Results
```bash
python evaluation/run_scoring.py
```

This will:
- Load results from `evaluation/results.json`
- Calculate all metrics for each result
- Save scored results to `evaluation/scored_results.json`
- Display average metrics

**Output:** `evaluation/scored_results.json` with all metrics

### Quick Run (Both Steps)
```bash
# Run both generation and scoring
python evaluation/run_generation.py && python evaluation/run_scoring.py
```

## Evaluation Queries

The evaluation uses 18 diverse Ubuntu technical support queries in `evaluation/data/eval_queries.json`:

- WiFi connectivity issues
- Boot problems
- Package management
- Bluetooth issues
- Disk space warnings
- Firewall configuration
- Hardware issues (touchpad, screen)
- System administration
- And more...

## Understanding Results

### Results File Structure

**`evaluation/results.json`:**
```json
[
  {
    "id": "Q1",
    "query": "I am not able to install python on my Ubuntu system",
    "context": "Retrieved context from vector store...",
    "answer": "Generated answer...",
    "similarity": 0.5970
  }
]
```

**`evaluation/scored_results.json`:**
```json
[
  {
    "id": "Q1",
    "query": "...",
    "context": "...",
    "answer": "...",
    "similarity": 0.5970,
    "metrics": {
      "context_relevance": 0.0,
      "faithfulness": 0.0,
      "hallucination_rate": 1.0,
      "answer_relevance": 0.0,
      "precision": 0.8,
      "recall": 0.0
    }
  }
]
```

### Interpreting Scores

**Good Performance:**
- Context Relevance: > 0.7
- Faithfulness: > 0.8
- Hallucination Rate: < 0.2
- Answer Relevance: > 0.85
- Precision: > 0.8
- Recall: > 0.6

**Poor Performance:**
- Context Relevance: < 0.5
- Faithfulness: < 0.5
- Hallucination Rate: > 0.5
- Answer Relevance: < 0.5
- Precision: < 0.5
- Recall: < 0.3

## Improvements Made

### Fixed Issues:
1. ✅ **Faithfulness Bug**: Now evaluates ALL claims, not just the last one
2. ✅ **Recall Type**: Returns float instead of string
3. ✅ **File Path**: Uses `results.json` instead of hardcoded `results1.json`
4. ✅ **Error Handling**: Graceful error handling with default values
5. ✅ **Progress Tracking**: Clear progress indicators
6. ✅ **Average Metrics**: Displays average scores across all queries

### Enhanced Features:
- Comprehensive documentation
- Better logging and progress tracking
- Error recovery
- Summary statistics
- Clear output formatting

## Troubleshooting

### Error: "results.json not found"
**Solution:** Run `python evaluation/run_generation.py` first

### Error: "eval_queries.json not found"
**Solution:** Ensure you're running from the project root directory

### Slow Evaluation
**Reason:** Each metric requires LLM calls
**Tip:** Start with fewer queries for testing, then run full evaluation

### Inconsistent Scores
**Reason:** LLM-based evaluation can have variance
**Tip:** Run multiple times and average the results

## Customization

### Add New Queries
Edit `evaluation/data/eval_queries.json`:
```json
{
  "id": "Q19",
  "query": "Your new query here"
}
```

### Modify Metrics
Edit files in `evaluation/metrics/`:
- `context_relevance.py`
- `faithfulness.py`
- `answer_relevance.py`
- `precision_recall.py`

### Change Evaluation Model
Edit `evaluation/utils/llm_judge.py` to use a different model

## Best Practices

1. **Baseline First**: Run evaluation before making changes
2. **Track Changes**: Save results with timestamps
3. **Compare**: Use diff tools to compare before/after results
4. **Iterate**: Make small changes and re-evaluate
5. **Document**: Note what changes improved which metrics

## Example Workflow

```bash
# 1. Baseline evaluation
python evaluation/run_generation.py
python evaluation/run_scoring.py
cp evaluation/scored_results.json evaluation/baseline_results.json

# 2. Make improvements to your RAG system
# (e.g., improve prompts, adjust retrieval, etc.)

# 3. Re-evaluate
python evaluation/run_generation.py
python evaluation/run_scoring.py

# 4. Compare results
# Compare evaluation/baseline_results.json with evaluation/scored_results.json
```

## Files Structure

```
evaluation/
├── README.md                    # This file
├── run_generation.py            # Step 1: Generate responses
├── run_scoring.py               # Step 2: Score responses
├── results.json                 # Generated responses
├── scored_results.json          # Scored results with metrics
├── data/
│   └── eval_queries.json        # Evaluation queries
├── metrics/
│   ├── context_relevance.py     # Context relevance metric
│   ├── faithfulness.py          # Faithfulness metric
│   ├── answer_relevance.py      # Answer relevance metric
│   └── precision_recall.py      # Precision & recall metrics
└── utils/
    ├── llm_judge.py             # LLM-based evaluation
    ├── claim_extractor.py       # Extract claims from text
    └── number_extractor.py      # Extract scores from LLM output
```

## Next Steps

After running evaluation:
1. Identify weak areas (low scores)
2. Make targeted improvements
3. Re-evaluate to measure impact
4. Iterate until targets are met

Good luck with your evaluation! 🚀