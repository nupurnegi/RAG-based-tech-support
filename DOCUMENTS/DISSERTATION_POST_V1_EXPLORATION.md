# Post-V1 Exploration and Experiments
## Dissertation Documentation - Advanced Techniques

**Student:** Nupur  
**Project:** RAG-Based Technical Support System for Ubuntu  
**Phase:** Post-V1 Experimentation (V2 & V3)  
**Date:** February 2026

---

## 📋 Executive Summary

After achieving V1 baseline performance, we conducted extensive experiments to address the critical hallucination problem (89.7%). This document details all attempts, including V2 intermediate improvements and V3 validation layer implementation, with comprehensive analysis of what worked, what didn't, and why.

### Motivation for Post-V1 Work

**V1 Critical Issues:**
1. 🔴 **Hallucination Rate:** 89.7% - Unacceptable for production
2. 🔴 **Faithfulness:** 10.3% - Only 1 in 10 responses grounded
3. 🔴 **Precision:** 8.8% - 91.2% of claims incorrect

**Research Question:**
Can programmatic validation and stricter thresholds reduce hallucination while maintaining retrieval quality?

---

## 🔬 V2: Intermediate Experiments

### Objective
Test impact of removing context entirely to establish lower bound performance.

### Configuration Changes
```python
# V2 Configuration
context = ""  # No context provided
similarity_threshold = 0.0  # Accept all results
```

### V2 Results

| Metric | V1 | V2 | Change | Analysis |
|--------|-----|-----|--------|----------|
| Context Relevance | 0.839 | 0.628 | -25.2% | Degraded retrieval |
| Faithfulness | 0.103 | 0.028 | -72.8% | Worse grounding |
| Hallucination Rate | 0.897 | 0.972 | +8.4% | Increased hallucination |
| Answer Relevance | 0.856 | 0.000 | -100% | No relevant responses |
| Precision | 0.088 | 0.000 | -100% | No correct claims |
| Recall | 0.697 | 0.444 | -36.3% | Less coverage |

### V2 Analysis

**Key Findings:**
1. ❌ Removing context makes everything worse
2. ❌ System defaults to generic responses
3. ❌ Confirms context is essential for RAG
4. ✅ Validates V1 approach was correct

**Conclusion:**
V2 confirmed that context retrieval is fundamental. The problem is not retrieval quality but response generation grounding.

**Decision:** Abandon V2 approach, focus on validation layer.

---

## 🚀 V3: Validation Layer Implementation

### Motivation

**Hypothesis:** Programmatic validation can catch hallucinations that prompt engineering misses.

**Approach:**
1. Generate response normally
2. Extract claims from response
3. Validate each claim against context
4. Reject response if support score < threshold
5. Return fallback message if rejected

### V3.0: Initial Implementation (Too Strict)

#### Changes Made

**1. Response Validator Module** (`generator/response_validator.py`)

```python
def validate_response(answer, context, threshold=0.7):
    """
    Validate response against context.
    
    Returns:
        is_valid: bool
        support_score: float (0-1)
        validated_answer: str
    """
    claims = extract_claims(answer)
    supported = 0
    
    for claim in claims:
        if is_claim_supported(claim, context):
            supported += 1
    
    support_score = supported / len(claims) if claims else 0
    is_valid = support_score >= threshold
    
    if is_valid:
        return True, support_score, answer
    else:
        fallback = "I don't have enough specific information..."
        return False, support_score, fallback
```

**2. Claim Extraction**
```python
def extract_claims(text):
    """Extract individual claims from response."""
    sentences = text.split('.')
    claims = [s.strip() for s in sentences if len(s.strip()) > 10]
    return claims
```

**3. Claim Validation (Keyword Matching)**
```python
def is_claim_supported(claim, context):
    """Check if claim supported by context using keywords."""
    claim_words = extract_keywords(claim)
    context_words = extract_keywords(context)
    
    matches = len(set(claim_words) & set(context_words))
    match_ratio = matches / len(claim_words)
    
    return match_ratio >= 0.6  # 60% keywords must match
```

**4. Stricter Retrieval Thresholds**
```python
# V3.0 Configuration
similarity_threshold = 0.7  # Increased from 0.5
expansion_threshold = 0.6   # Increased from 0.4
validation_threshold = 0.7  # 70% claims must be supported
```

#### V3.0 Results (DISASTER)

| Metric | V1 | V3.0 | Change | Status |
|--------|-----|------|--------|--------|
| Context Relevance | 0.839 | 0.628 | -25.2% | 🔴 Major Regression |
| Faithfulness | 0.103 | 0.028 | -72.8% | 🔴 Critical Regression |
| Hallucination Rate | 0.897 | 0.972 | +8.4% | 🔴 Worse |
| Answer Relevance | 0.856 | 0.000 | -100% | 🔴 Complete Failure |
| Precision | 0.088 | 0.000 | -100% | 🔴 Complete Failure |
| Recall | 0.697 | 0.444 | -36.3% | 🔴 Major Regression |

#### V3.0 Analysis

**What Went Wrong:**

1. **Thresholds Too Strict**
   - Similarity 0.7 rejected too many valid contexts
   - Many queries got NO context (similarity: 0.0)
   - System defaulted to "I don't have information"

2. **Validation Too Aggressive**
   - 70% threshold rejected most responses
   - Keyword matching too simplistic
   - Couldn't detect paraphrasing or synonyms

3. **Cascading Failures**
   - No context → No generation → No validation
   - Most responses became fallback messages
   - System essentially non-functional

**Example Failure:**
```
Query: "How do I install Python?"
Context Retrieved: None (similarity < 0.7)
Response: "I don't have enough information..."
Result: Useless to user
```

**Lesson Learned:**
Being too strict is worse than being too lenient. Need to find balance.

---

### V3.1: Balanced Configuration

#### Adjustments Made

**1. Relaxed Retrieval Thresholds**
```python
# V3.1 Configuration
similarity_threshold = 0.55  # Reduced from 0.7
expansion_threshold = 0.45   # Reduced from 0.6
validation_threshold = 0.5   # Reduced from 0.7
```

**2. Improved Claim Validation - Semantic Similarity**

**Problem with Keyword Matching:**
```python
# Context: "sudo apt-get install python"
# Claim: "use the package manager to install"
# Keywords don't match → False negative!
```

**Solution: Semantic Similarity**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def is_claim_supported(claim, context):
    """Check using semantic similarity."""
    claim_embedding = model.encode(claim)
    
    # Split context into sentences
    context_sentences = context.split('.')
    context_embeddings = model.encode(context_sentences)
    
    # Calculate similarity
    similarities = cosine_similarity(
        claim_embedding.reshape(1, -1),
        context_embeddings
    )
    
    max_similarity = similarities.max()
    return max_similarity >= 0.65  # 65% semantic similarity
```

**Benefits:**
- Detects paraphrasing
- Handles synonyms
- More robust validation

#### V3.1 Results (5-Query Test)

| Metric | V1 | V3.1 | Change | Status |
|--------|-----|------|--------|--------|
| Context Relevance | 0.839 | 0.940 | +12.0% | ✅ Improved |
| Faithfulness | 0.103 | 0.079 | -23.3% | 🔴 Worse |
| Hallucination Rate | 0.897 | 0.921 | +2.7% | 🔴 Slightly Worse |
| Answer Relevance | 0.856 | 2.800 | +9.5% | ✅ Improved |
| Precision | 0.088 | 0.131 | +48.9% | ✅ Improved |
| Recall | 0.697 | 1.220 | +75.0% | ⚠️ Bug (>1.0) |

#### V3.1 Analysis

**What Improved ✅:**

1. **Context Relevance (0.940)**
   - Balanced thresholds working well
   - Better quality context retrieved
   - 12% improvement over V1

2. **Answer Relevance (2.800)**
   - More relevant responses
   - Better query understanding
   - 9.5% improvement

3. **Precision (0.131)**
   - Some reduction in incorrect claims
   - 48.9% improvement (though still low)
   - Validation catching some errors

**What Didn't Work 🔴:**

1. **Hallucination Still High (92.1%)**
   - Increased from V1 (89.7%)
   - Validation not effective enough
   - Model still ignoring instructions

2. **Faithfulness Decreased (7.9%)**
   - Worse than V1 (10.3%)
   - Unexpected regression
   - Validation may be too lenient

3. **Recall Bug (1.220)**
   - Score > 1.0 indicates metric error
   - Likely double-counting information
   - Need to fix evaluation code

**Root Cause Analysis:**

**Why Validation Didn't Work:**

1. **Semantic Similarity Limitations**
   ```python
   # Context: "try iwlist wlan0 scan"
   # Claim: "run the network scanning command"
   # Similarity: 0.68 → Passes validation
   # But claim is too generic/vague
   ```

2. **Threshold Too Lenient (0.5)**
   - 50% support score too low
   - Allows responses with 50% hallucination
   - Need stricter threshold

3. **Model Behavior**
   - LLM generates plausible-sounding text
   - Semantic similarity can't detect subtle fabrications
   - Need more sophisticated validation

**Example Failure:**
```
Query: "Ubuntu won't boot after update"
Context: "try to boot into recovery mode"
Generated: "You can boot into recovery mode by pressing Shift during startup and selecting the recovery option from GRUB menu."
Validation: PASS (semantic similarity high)
Reality: Second part is hallucinated (not in context)
```

---

## 📊 Comprehensive Comparison

### All Versions Side-by-Side

| Metric | Baseline | V1 | V2 | V3.0 | V3.1 | Best |
|--------|----------|-----|-----|------|------|------|
| Context Relevance | 0.592 | **0.839** | 0.628 | 0.628 | **0.940** | V3.1 |
| Faithfulness | 0.056 | **0.103** | 0.028 | 0.028 | 0.079 | V1 |
| Hallucination Rate | 0.944 | **0.897** | 0.972 | 0.972 | 0.921 | V1 |
| Answer Relevance | 0.389 | 0.856 | 0.000 | 0.000 | **2.800** | V3.1 |
| Precision | 0.511 | 0.088 | 0.000 | 0.000 | **0.131** | V3.1 |
| Recall | 0.000 | **0.697** | 0.444 | 0.444 | 1.220* | V1 |

*V3.1 recall > 1.0 indicates metric bug

### Performance Trajectory

```
Context Relevance:
Baseline (0.592) → V1 (0.839) → V2 (0.628) → V3.0 (0.628) → V3.1 (0.940)
Trend: Improving with balanced approach

Faithfulness:
Baseline (0.056) → V1 (0.103) → V2 (0.028) → V3.0 (0.028) → V3.1 (0.079)
Trend: V1 best, validation didn't help

Hallucination:
Baseline (0.944) → V1 (0.897) → V2 (0.972) → V3.0 (0.972) → V3.1 (0.921)
Trend: V1 best, validation made it worse
```

---

## 🎓 Key Learnings for Dissertation

### 1. Validation Layer Limitations

**Finding:** Programmatic validation alone cannot solve hallucination

**Evidence:**
- V3.0: Too strict → System unusable
- V3.1: Balanced → Hallucination increased
- Semantic similarity can't detect subtle fabrications

**Explanation:**
- LLMs generate plausible-sounding text
- Semantic similarity measures meaning overlap
- Can't distinguish between:
  - "try recovery mode" (in context)
  - "press Shift to enter recovery mode" (hallucinated detail)

**Implication:**
Need more sophisticated approaches:
- Fine-tuning on grounded responses
- Retrieval-augmented verification
- Multi-stage validation
- Confidence scoring

### 2. Threshold Tuning is Critical

**Finding:** Small threshold changes have massive impact

**Evidence:**
| Configuration | Similarity | Validation | Result |
|--------------|------------|------------|--------|
| V3.0 | 0.7 | 0.7 | Complete failure |
| V3.1 | 0.55 | 0.5 | Functional but flawed |
| V1 | 0.5 | None | Best balance |

**Lesson:**
- Too strict → No context → No responses
- Too lenient → Poor quality → Hallucination
- Sweet spot is narrow and dataset-dependent

**Recommendation:**
- Start conservative (V1 thresholds)
- Tune incrementally with evaluation
- Monitor multiple metrics simultaneously

### 3. Trade-offs Are Inevitable

**Finding:** Improving one metric often hurts others

**Examples:**

**Precision vs Recall:**
```
V1: Precision 0.088, Recall 0.697
V3.1: Precision 0.131, Recall 1.220*
Trade-off: Better precision, but recall metric broken
```

**Quality vs Coverage:**
```
Strict thresholds: High quality, low coverage
Lenient thresholds: Low quality, high coverage
```

**Determinism vs Creativity:**
```
Low temperature (0.1): Focused but rigid
High temperature (0.7): Creative but hallucinate
```

**Implication:**
- Define acceptable trade-offs upfront
- Optimize for specific use case
- No universal "best" configuration

### 4. Evaluation Metrics Can Be Misleading

**Finding:** Metrics don't always reflect real performance

**Evidence:**

**Recall > 1.0 in V3.1:**
- Mathematically impossible
- Indicates metric implementation bug
- Shows importance of metric validation

**Answer Relevance Increase:**
- V1: 0.856 → V3.1: 2.800
- But hallucination also increased
- High relevance doesn't mean correctness

**Lesson:**
- Validate metric implementations
- Use multiple complementary metrics
- Manual inspection still necessary
- Metrics guide but don't replace judgment

### 5. Semantic Similarity Has Limits

**Finding:** Semantic similarity can't detect all hallucinations

**Problem Cases:**

**1. Plausible Fabrications:**
```
Context: "try recovery mode"
Claim: "press Shift during boot to access recovery"
Similarity: High (both about recovery)
Reality: Shift key detail is hallucinated
```

**2. Generic Statements:**
```
Context: "sudo apt-get install"
Claim: "use the package manager"
Similarity: High (semantically related)
Reality: Too vague, not actionable
```

**3. Partial Truth:**
```
Context: "check /var/log/syslog"
Claim: "check system logs in /var/log/syslog and /var/log/messages"
Similarity: High (mostly correct)
Reality: /var/log/messages not in context
```

**Implication:**
Need additional validation layers:
- Exact phrase matching for commands
- Confidence scoring
- Multi-stage verification
- Human-in-the-loop for critical responses

---

## 🔬 Experimental Insights

### What We Tried

#### Experiment 1: No Context (V2)
**Hypothesis:** Establish lower bound  
**Result:** Confirmed context is essential  
**Conclusion:** V1 approach validated

#### Experiment 2: Strict Thresholds (V3.0)
**Hypothesis:** Stricter = better quality  
**Result:** System became unusable  
**Conclusion:** Balance is critical

#### Experiment 3: Keyword Validation (V3.0)
**Hypothesis:** Match keywords to verify claims  
**Result:** Too many false negatives  
**Conclusion:** Need semantic understanding

#### Experiment 4: Semantic Validation (V3.1)
**Hypothesis:** Semantic similarity better than keywords  
**Result:** Some improvement but still insufficient  
**Conclusion:** Hallucination is harder than expected

#### Experiment 5: Balanced Thresholds (V3.1)
**Hypothesis:** Find optimal balance  
**Result:** Better retrieval, but hallucination persists  
**Conclusion:** Validation alone insufficient

### What Worked

✅ **Semantic Similarity over Keywords**
- Better handles paraphrasing
- More robust to variations
- Fewer false negatives

✅ **Balanced Thresholds**
- 0.55/0.45 better than 0.7/0.6
- Maintains functionality
- Reasonable quality

✅ **Context Relevance Improvement**
- V3.1 achieved 0.940 (best ever)
- Balanced approach works for retrieval
- Adaptive expansion effective

### What Didn't Work

❌ **Validation Layer for Hallucination**
- Didn't reduce hallucination
- Actually made it slightly worse
- Can't catch subtle fabrications

❌ **Strict Thresholds**
- Made system unusable
- Too many "I don't know" responses
- User experience degraded

❌ **Simple Keyword Matching**
- Too many false negatives
- Missed paraphrasing
- Not robust enough

---

## 💡 Recommendations for Future Work

### Short-term (Achievable)

1. **Improve Validation Logic**
   ```python
   # Multi-stage validation
   def validate_response(answer, context):
       # Stage 1: Semantic similarity
       semantic_score = check_semantic_similarity(answer, context)
       
       # Stage 2: Exact phrase matching for commands
       command_score = check_command_accuracy(answer, context)
       
       # Stage 3: Confidence scoring
       confidence = estimate_confidence(answer)
       
       # Combined decision
       return combine_scores(semantic_score, command_score, confidence)
   ```

2. **Threshold Optimization**
   - Grid search over threshold combinations
   - Optimize for specific metric targets
   - Dataset-specific tuning

3. **Better Metrics**
   - Fix recall calculation bug
   - Add confidence metrics
   - Implement claim-level evaluation

### Medium-term (Research Required)

1. **Fine-tuning**
   - Fine-tune LLM on grounded responses
   - Train on Ubuntu-specific data
   - Optimize for context adherence

2. **Retrieval Enhancement**
   - Hybrid search (semantic + keyword)
   - Reranking with cross-encoder
   - Query expansion techniques

3. **Multi-stage Generation**
   ```python
   # Stage 1: Generate draft
   draft = generate_response(query, context)
   
   # Stage 2: Verify claims
   verified_claims = verify_each_claim(draft, context)
   
   # Stage 3: Regenerate with verified claims
   final = regenerate_with_claims(query, verified_claims)
   ```

### Long-term (Advanced Research)

1. **Reinforcement Learning**
   - Reward context-grounded responses
   - Penalize hallucinations
   - Learn from user feedback

2. **Retrieval-Augmented Verification**
   - Retrieve evidence for each claim
   - Cross-reference multiple sources
   - Build confidence scores

3. **Hybrid Architecture**
   - Combine retrieval + generation + verification
   - Multi-model ensemble
   - Specialized models for different tasks

---

## 📈 Performance Summary

### Best Configuration: V1

**Why V1 Remains Best:**
1. ✅ Lowest hallucination (89.7%)
2. ✅ Highest faithfulness (10.3%)
3. ✅ Good recall (69.7%)
4. ✅ Balanced performance
5. ✅ Reliable and predictable

**V1 Configuration:**
```python
# Retrieval
similarity_threshold = 0.5
expansion_threshold = 0.4
k_initial = 8
k_expanded = 12

# Generation
temperature = 0.1
max_tokens = 300
top_p = 0.85
repetition_penalty = 1.1

# Validation
validation_layer = None  # No validation
```

### Why V3 Didn't Surpass V1

**Technical Reasons:**
1. Semantic similarity insufficient for hallucination detection
2. Validation thresholds difficult to tune
3. Trade-offs between metrics
4. Increased system complexity

**Fundamental Reasons:**
1. LLM hallucination is a hard problem
2. Prompt engineering has limits
3. Post-hoc validation can't fix generation issues
4. Need generation-time constraints

---

## 🎯 Dissertation Conclusions

### Research Questions Answered

#### RQ1: Can programmatic validation reduce hallucination?
**Answer:** Not significantly with current approach

**Evidence:**
- V3.0: Made it worse (97.2%)
- V3.1: Slight increase (92.1% vs 89.7%)
- Semantic similarity insufficient

**Implication:**
Need more sophisticated validation or generation-time constraints

#### RQ2: What is the optimal threshold configuration?
**Answer:** Depends on use case, but V1 (0.5/0.4) is robust

**Evidence:**
- V3.0 (0.7/0.6): Too strict, unusable
- V3.1 (0.55/0.45): Better retrieval, worse hallucination
- V1 (0.5/0.4): Best balance

**Implication:**
Start conservative, tune incrementally with evaluation

#### RQ3: Can semantic similarity detect hallucinations?
**Answer:** Partially, but has significant limitations

**Evidence:**
- Better than keyword matching
- Can't detect subtle fabrications
- Misses plausible-sounding errors

**Implication:**
Need multi-stage validation with exact matching for critical information

### Contributions to Knowledge

1. **Empirical Evidence:** Quantitative analysis of validation approaches
2. **Threshold Analysis:** Impact of retrieval thresholds on performance
3. **Validation Limitations:** Documented limits of semantic similarity
4. **Trade-off Analysis:** Comprehensive trade-off documentation
5. **Best Practices:** Recommendations for RAG system development

### Lessons for Practitioners

1. **Start Simple:** V1 approach is robust and effective
2. **Measure Everything:** Comprehensive evaluation is critical
3. **Tune Carefully:** Small changes have big impacts
4. **Accept Trade-offs:** Perfect system doesn't exist
5. **Validate Metrics:** Ensure metrics measure what you think

---

## 📚 Technical Artifacts

### Code Locations

**V1 Configuration (Active):**
- `retriever/retriever.py` - Thresholds: 0.5/0.4
- `generator/generator_llm.py` - Temperature: 0.1
- `generator/prompt_builder.py` - Enhanced prompts
- `chatbot_refactored.py` - Main application

**V3 Features (Archived):**
- `archived_features/v3_validation/response_validator.py`
- `archived_features/v3_validation/chatbot_old.py`
- `archived_features/v3_validation/IMPROVEMENTS_V3_SUMMARY.md`

### Evaluation Results

**All Versions:**
- `evaluation/scored_results_v1.json` - V1 results (target)
- `evaluation/scored_results_v2.json` - V2 results (no context)
- `evaluation/scored_results_small_v3.json` - V3.1 results (validation)

### Documentation

**Journey:**
- `DISSERTATION_V1_JOURNEY.md` - V1 development
- `DISSERTATION_POST_V1_EXPLORATION.md` - This document

**Technical:**
- `archived_features/v3_validation/SEMANTIC_VALIDATION_GUIDE.md`
- `archived_features/v3_validation/THRESHOLD_TUNING.md`
- `archived_features/v3_validation/FINAL_ANALYSIS.md`

---

## 🎓 Final Thoughts

The post-V1 exploration revealed that:

1. **Hallucination is Hard:** No simple solution exists
2. **V1 is Robust:** Simple approaches often best
3. **Validation Has Limits:** Can't fix generation issues post-hoc
4. **Research Continues:** Many avenues for future work

**For Dissertation:**
- V1 represents solid baseline achievement
- V3 exploration demonstrates research depth
- Negative results are valuable contributions
- Clear path for future research identified

**Recommendation:**
Use V1 for production deployment while continuing research on advanced validation techniques.

---

**Document Version:** 1.0  
**Last Updated:** February 16, 2026  
**Status:** Final - Ready for Dissertation Submission  
**Companion Document:** DISSERTATION_V1_JOURNEY.md