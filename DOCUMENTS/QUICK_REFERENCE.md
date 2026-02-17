# Quick Reference Guide - RAG System Improvements

## 🚀 Quick Start

### Run Evaluation
```bash
# Generate responses
python evaluation/run_generation.py

# Score responses
python evaluation/run_scoring.py
```

### Run Application
```bash
python chatbot.py
# or
python chatbot_refactored.py
```

---

## 📊 Key Metrics to Monitor

| Metric | Target | What It Measures |
|--------|--------|------------------|
| **Faithfulness** | > 0.8 | Answer grounded in context |
| **Hallucination Rate** | < 0.2 | Fabricated information |
| **Context Relevance** | > 0.7 | Quality of retrieval |
| **Answer Relevance** | > 0.85 | Addresses user query |
| **Precision** | > 0.8 | Correct claims |
| **Recall** | > 0.6 | Information coverage |

---

## 🔧 Key Configuration Parameters

### Retrieval (`retriever/retriever.py`)
```python
k = 8                      # Number of documents to retrieve
similarity_threshold = 0.5  # Minimum similarity score
expansion_k = 12           # Expanded retrieval if needed
expansion_threshold = 0.4  # Lower threshold for expansion
```

### Generation (`generator/generator_llm.py`)
```python
max_new_tokens = 300       # Response length
temperature = 0.1          # Determinism (lower = more factual)
repetition_penalty = 1.1   # Reduce repetition
decoding_method = "greedy" # Most likely tokens
```

### Intent Classification (`context_expansion/intent_analyzer.py`)
```python
# Classifies queries as CLEAR or AMBIGUOUS
# AMBIGUOUS queries trigger follow-up questions
```

---

## 🐛 Common Issues & Solutions

### Issue: Application Crashes
**Solution:** Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: High Hallucination
**Solutions:**
1. Lower temperature (currently 0.1)
2. Strengthen prompt rules
3. Improve context quality
4. Increase similarity threshold

### Issue: Poor Context Retrieval
**Solutions:**
1. Adjust similarity threshold
2. Increase k value
3. Improve query preprocessing
4. Consider query expansion

### Issue: Truncated Responses
**Solution:** Increase `max_new_tokens` (currently 300)

---

## 📁 File Structure

```
RAG-based-tech-support/
├── chatbot.py                      # Main application
├── chatbot_refactored.py           # Modular version
├── requirements.txt                # Dependencies
├── README.md                       # Project documentation
├── IMPROVEMENTS_SUMMARY.md         # Detailed improvements
├── QUICK_REFERENCE.md              # This file
│
├── retriever/
│   ├── retriever.py                # Context retrieval logic
│   └── vector_store.py             # Milvus connection
│
├── generator/
│   ├── generator_llm.py            # LLM initialization
│   └── prompt_builder.py           # Prompt construction
│
├── context_expansion/
│   ├── intent_analyzer.py          # Intent classification
│   ├── intent_llm.py               # LLM for intent
│   └── intent_prompt.py            # Intent prompts
│
├── evaluation/
│   ├── README.md                   # Evaluation guide
│   ├── run_generation.py           # Generate responses
│   ├── run_scoring.py              # Calculate metrics
│   ├── results.json                # Generated responses
│   ├── scored_results.json         # Scored results
│   ├── data/
│   │   └── eval_queries.json       # Test queries
│   ├── metrics/
│   │   ├── context_relevance.py
│   │   ├── faithfulness.py
│   │   ├── answer_relevance.py
│   │   └── precision_recall.py
│   └── utils/
│       ├── llm_judge.py
│       ├── claim_extractor.py
│       └── number_extractor.py
│
├── utils/                          # NEW
│   ├── constants.py                # Configuration
│   └── helpers.py                  # Utility functions
│
├── ui/                             # NEW
│   └── gradio_interface.py         # UI components
│
└── data_prep/
    ├── data_loader.py              # Load dataset
    ├── data_embedding.py           # Create embeddings
    ├── insert_data.py              # Insert to Milvus
    └── store_data.py               # Store management
```

---

## 🎯 Improvement Checklist

### ✅ Completed
- [x] Fixed critical bugs (retrieve_context, intent classification)
- [x] Enhanced prompt engineering
- [x] Optimized generator parameters
- [x] Fixed evaluation metrics
- [x] Added comprehensive documentation
- [x] Refactored codebase

### 🔄 In Progress
- [ ] Running evaluation pipeline
- [ ] Analyzing results

### 📋 Pending
- [ ] Query expansion
- [ ] Reranking
- [ ] Response validation
- [ ] Confidence scoring
- [ ] Automated testing

---

## 💡 Best Practices

### 1. Always Evaluate Before Changes
```bash
# Baseline
python evaluation/run_generation.py
python evaluation/run_scoring.py
cp evaluation/scored_results.json baseline_results.json
```

### 2. Make Small, Measurable Changes
- Change one parameter at a time
- Re-evaluate after each change
- Document what worked

### 3. Monitor Key Metrics
- Focus on faithfulness (hallucination)
- Track context relevance (retrieval quality)
- Measure answer relevance (user satisfaction)

### 4. Use Version Control
```bash
git add .
git commit -m "Improved prompt engineering - reduced hallucination by X%"
```

---

## 🔍 Debugging Tips

### Check Vector Store Connection
```python
from retriever.vector_store import get_vectorstore
vectorstore = get_vectorstore()
print(f"Collection count: {vectorstore.col.num_entities}")
```

### Test Single Query
```python
from retriever.retriever import retrieve_context
context, similarity = retrieve_context(vectorstore, "test query")
print(f"Context: {context[:200]}...")
print(f"Similarity: {similarity}")
```

### Verify LLM Connection
```python
from generator.generator_llm import get_llm
llm = get_llm()
response = llm.generate(["Test prompt"])
print(response)
```

---

## 📞 Support

### Documentation
- `README.md` - Project overview
- `evaluation/README.md` - Evaluation guide
- `IMPROVEMENTS_SUMMARY.md` - Detailed changes

### Key Concepts
- **RAG**: Retrieval-Augmented Generation
- **Hallucination**: Model generating false information
- **Faithfulness**: Answer grounded in context
- **Context Relevance**: Quality of retrieved documents

---

## 🎓 Learning Resources

### Understanding RAG
- Retrieval: Finding relevant documents
- Augmentation: Adding context to prompt
- Generation: LLM creates response

### Reducing Hallucination
1. **Prompt Engineering**: Clear instructions
2. **Temperature Control**: Lower = more factual
3. **Context Quality**: Better retrieval
4. **Response Validation**: Check grounding

### Evaluation Metrics
- **Precision**: Correctness of claims
- **Recall**: Coverage of information
- **Faithfulness**: Grounding in context
- **Relevance**: Addressing the query

---

## 🚦 Status Indicators

### System Health
- ✅ **Green**: All metrics above targets
- ⚠️ **Yellow**: Some metrics below targets
- 🔴 **Red**: Critical metrics failing

### Current Status
- **Faithfulness**: 🔄 Evaluating...
- **Context Relevance**: 🔄 Evaluating...
- **Answer Relevance**: 🔄 Evaluating...

---

## 📈 Next Steps

1. ✅ Complete evaluation run
2. 📊 Analyze results
3. 🎯 Identify weak areas
4. 🔧 Make targeted improvements
5. 🔄 Re-evaluate
6. 📝 Document findings

---

**Last Updated:** 2026-02-16  
**Version:** 2.0 (Post-improvements)