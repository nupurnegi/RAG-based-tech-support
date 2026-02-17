# V3 Validation Features (Archived)

This folder contains the V3 validation layer features that were removed when reverting to V1 configuration.

## Contents

### Code Files:
1. **response_validator.py** - Response validation module
   - Extract claims from generated responses
   - Validate claims against retrieved context
   - Calculate support scores
   - Filter unsupported claims
   - Provide fallback messages for low-quality responses

2. **chatbot_old.py** - Original chatbot.py with V3 validation integrated

### Documentation Files:
1. **IMPROVEMENTS_V3_SUMMARY.md** - Complete V3 improvements documentation
   - Response validation layer implementation
   - Enhanced prompt engineering
   - Stricter similarity thresholds
   - Integration details
   - Expected performance improvements

2. **SEMANTIC_VALIDATION_GUIDE.md** - Semantic similarity validation guide
   - Technical implementation details
   - Comparison with keyword matching
   - Embedding-based validation approach

3. **THRESHOLD_TUNING.md** - Threshold optimization guide
   - Problem identification with strict thresholds
   - Adjustments made to balance performance
   - Tuning recommendations

4. **FINAL_ANALYSIS.md** - Final performance analysis
   - V3.1 balanced results
   - What worked and what didn't
   - Key findings and insights

5. **HONEST_ASSESSMENT.md** - Honest assessment of system performance

### Evaluation Results:
- `scored_results_small_v3.json` - Scored results with V3 validation
- `results_small_v3.json` - Raw results with V3 validation

## Why These Were Archived

The system was reverted to V1 configuration to achieve the target scores:
- Context Relevance: 0.839
- Faithfulness: 0.103
- Hallucination Rate: 0.897
- Answer Relevance: 0.856
- Precision: 0.088
- Recall: 0.697

V3 validation layer, while reducing hallucination, changed the score profile significantly.

## How to Restore V3 Features

If you want to re-enable V3 validation:

1. **Move response_validator.py back:**
   ```bash
   mv archived_features/v3_validation/response_validator.py generator/
   ```

2. **Update chatbot.py:**
   ```python
   from generator.response_validator import validate_response
   
   # After generating response:
   is_valid, support_score, validated_response = validate_response(
       response, context, threshold=0.5
   )
   response = validated_response
   ```

3. **Update evaluation/run_generation.py:**
   ```python
   from generator.response_validator import validate_response
   
   # In run_rag function:
   is_valid, support_score, validated_answer = validate_response(
       answer, context, threshold=0.5
   )
   
   return {
       "query": query,
       "context": context,
       "answer": validated_answer,
       "similarity": similarity,
       "support_score": support_score,
       "validation_passed": is_valid
   }
   ```

4. **Update retriever thresholds in retriever/retriever.py:**
   ```python
   relevant_docs = [(d, score) for d, score in docs_with_scores if score > 0.55]
   # expansion threshold: 0.45
   ```

## Version History

- **V1** (Current): Original configuration with target scores
- **V2**: Intermediate improvements
- **V3** (Archived): Added validation layer for hallucination reduction

## Date Archived
2026-02-16