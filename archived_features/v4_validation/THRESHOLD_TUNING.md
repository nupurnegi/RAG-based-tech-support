# Threshold Tuning Guide

## 🎯 Problem Identified

After implementing V3 improvements with strict thresholds, we saw a **huge regression**:

### V3 Initial Results (TOO STRICT):
- Context Relevance: 0.628 (down from 0.839)
- Faithfulness: 0.028 (down from 0.103)
- Hallucination Rate: 0.972 (up from 0.897)
- Answer Relevance: 0.000 (down from 0.856)
- Precision: 0.000 (down from 0.088)
- Recall: 0.444 (down from 0.697)

**Root Cause:** Thresholds were too aggressive, causing:
1. Many queries got NO context (similarity: 0.0)
2. Valid responses were rejected by validation
3. Most responses became "I don't have enough information"

---

## ✅ Adjustments Made

### 1. Similarity Thresholds (retriever/retriever.py)

**Before (TOO STRICT):**
```python
similarity_threshold = 0.7  # Initial retrieval
expansion_threshold = 0.6   # Expansion if needed
```

**After (BALANCED):**
```python
similarity_threshold = 0.55  # Initial retrieval (was 0.7)
expansion_threshold = 0.45   # Expansion if needed (was 0.6)
```

**Rationale:**
- 0.7 was too high - many queries got zero results
- 0.55 provides good balance between quality and coverage
- Still higher than original 0.5, but not overly restrictive

---

### 2. Validation Threshold (all application files)

**Before (TOO STRICT):**
```python
validate_response(response, context, threshold=0.6)
# Required 60% of claims to be supported
```

**After (BALANCED):**
```python
validate_response(response, context, threshold=0.4)
# Requires 40% of claims to be supported
```

**Rationale:**
- 60% was rejecting too many valid responses
- 40% still provides validation but is more lenient
- Allows responses with partial grounding to pass

---

### 3. Keyword Matching Logic (response_validator.py)

**Before:**
```python
match_ratio = matches / len(claim_words)
return match_ratio >= 0.6  # 60% of keywords must match
```

**After:**
```python
# Special handling for short claims
if len(claim_words) <= 2:
    return matches >= 1  # At least one word must match

match_ratio = matches / len(claim_words)
return match_ratio >= 0.4  # 40% of keywords must match (was 60%)
```

**Improvements:**
- More lenient matching (40% vs 60%)
- Special case for short claims
- Added more stop words to filter

---

## 📊 Expected Results After Tuning

### Target Metrics:
| Metric | V2 Baseline | V3 Too Strict | V3 Balanced (Expected) |
|--------|-------------|---------------|------------------------|
| Context Relevance | 0.839 | 0.628 | **0.80+** |
| Faithfulness | 0.103 | 0.028 | **0.30+** |
| Hallucination Rate | 0.897 | 0.972 | **0.70-** |
| Answer Relevance | 0.856 | 0.000 | **2.00+** |
| Precision | 0.088 | 0.000 | **0.30+** |
| Recall | 0.697 | 0.444 | **0.60+** |

**Goals:**
- ✅ Better than V2 baseline
- ✅ Not as restrictive as initial V3
- ✅ Balance between quality and coverage

---

## 🔧 Tuning Philosophy

### The Trade-off Triangle:
```
        Quality
         /\
        /  \
       /    \
      /      \
     /________\
Coverage    Validation
```

**Key Principles:**

1. **Too Strict = No Responses**
   - High thresholds → No context retrieved
   - Strict validation → All responses rejected
   - Result: "I don't know" for everything

2. **Too Lenient = Hallucination**
   - Low thresholds → Irrelevant context
   - Weak validation → Bad responses pass
   - Result: Fabricated information

3. **Balanced = Best Results**
   - Moderate thresholds → Good context
   - Reasonable validation → Quality control
   - Result: Helpful, grounded responses

---

## 🎯 Current Configuration

### Similarity Thresholds:
```python
# retriever/retriever.py
Initial: 0.55  # Good balance
Expansion: 0.45  # Fallback for difficult queries
```

### Validation Thresholds:
```python
# All application files
Validation: 0.4  # 40% of claims must be supported
Keyword Match: 0.4  # 40% of keywords must match
```

### When to Adjust:

**Increase thresholds if:**
- Too many hallucinated responses
- Low precision/faithfulness
- Responses going beyond context

**Decrease thresholds if:**
- Too many "I don't know" responses
- Low recall/coverage
- Missing relevant information

---

## 📈 Monitoring Guide

### Key Indicators:

1. **Context Retrieval Rate**
   ```python
   # Check how many queries get context
   queries_with_context = sum(1 for r in results if r['similarity'] > 0)
   rate = queries_with_context / len(results)
   # Target: > 80%
   ```

2. **Validation Pass Rate**
   ```python
   # Check how many responses pass validation
   passed = sum(1 for r in results if r['validation_passed'])
   rate = passed / len(results)
   # Target: 60-80%
   ```

3. **Support Score Distribution**
   ```python
   # Check average support score
   avg_support = sum(r['support_score'] for r in results) / len(results)
   # Target: 0.5-0.7
   ```

---

## 🔄 Iterative Tuning Process

### Step 1: Run Evaluation
```bash
python evaluation/run_generation.py
python evaluation/run_scoring.py
```

### Step 2: Analyze Results
- Check context retrieval rate
- Check validation pass rate
- Review sample responses

### Step 3: Adjust Thresholds
- If too many rejections → Lower thresholds
- If too much hallucination → Raise thresholds

### Step 4: Re-evaluate
- Run evaluation again
- Compare metrics
- Iterate until balanced

---

## 💡 Best Practices

### 1. Start Conservative
- Begin with moderate thresholds
- Gradually adjust based on results
- Don't make large jumps

### 2. Monitor Multiple Metrics
- Don't optimize for one metric alone
- Balance quality vs coverage
- Consider user experience

### 3. Test with Real Queries
- Use actual user questions
- Check edge cases
- Validate with domain experts

### 4. Document Changes
- Track threshold values
- Note reasons for changes
- Record results

---

## 📝 Threshold History

| Version | Similarity | Expansion | Validation | Keyword | Notes |
|---------|-----------|-----------|------------|---------|-------|
| V2 | 0.50 | 0.40 | N/A | N/A | Baseline |
| V3 Initial | 0.70 | 0.60 | 0.60 | 0.60 | Too strict |
| V3 Balanced | 0.55 | 0.45 | 0.40 | 0.40 | Current |

---

## 🎓 Lessons Learned

### What Worked:
1. ✅ Validation layer concept is sound
2. ✅ Enhanced prompts help guide model
3. ✅ Programmatic checks catch issues

### What Didn't Work:
1. ❌ Initial thresholds too aggressive
2. ❌ Didn't account for query diversity
3. ❌ Validation too strict for technical content

### Key Insights:
1. 💡 Balance is critical - not too strict, not too lenient
2. 💡 Different query types need different handling
3. 💡 Validation should enhance, not replace responses
4. 💡 Always test with real data before deploying

---

## 🚀 Next Steps

1. **Run New Evaluation**
   ```bash
   python evaluation/run_generation.py
   python evaluation/run_scoring.py
   ```

2. **Analyze Results**
   - Compare with V2 baseline
   - Check all metrics
   - Review sample responses

3. **Fine-tune if Needed**
   - Adjust thresholds based on results
   - Test edge cases
   - Validate with users

4. **Document Final Configuration**
   - Record optimal thresholds
   - Note any special cases
   - Create deployment guide

---

## 📞 Quick Reference

### Current Thresholds:
```python
# Retrieval
SIMILARITY_THRESHOLD = 0.55
EXPANSION_THRESHOLD = 0.45

# Validation
VALIDATION_THRESHOLD = 0.4
KEYWORD_MATCH_THRESHOLD = 0.4
```

### Files Modified:
- ✅ `retriever/retriever.py` - Similarity thresholds
- ✅ `generator/response_validator.py` - Validation logic
- ✅ `evaluation/run_generation.py` - Validation threshold
- ✅ `chatbot.py` - Validation threshold
- ✅ `chatbot_refactored.py` - Validation threshold

---

**Status:** Thresholds adjusted for better balance  
**Next:** Run evaluation to measure improvements  
**Goal:** Achieve better performance than V2 baseline