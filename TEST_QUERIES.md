# Test Queries for RAG System

Use these queries to test different aspects of your RAG-based technical support system.

## 🎯 Test Categories

### 1. **CLEAR Technical Queries** (Should be classified as CLEAR and get proper responses)

#### Basic Ubuntu Issues
```
1. "My WiFi is not connecting"
2. "Ubuntu won't boot after update"
3. "How do I install Python packages?"
4. "My system is running slow"
5. "Can't connect to Bluetooth device"
```

#### Specific Technical Problems
```
6. "Getting 'broken packages' error when running apt update"
7. "Touchpad stopped working after installing Ubuntu"
8. "How do I enable UFW firewall for SSH?"
9. "Disk space low warning on root partition"
10. "Sound not working through HDMI"
```

#### Command/Configuration Questions
```
11. "How to check disk space in Ubuntu?"
12. "What command shows network interfaces?"
13. "How do I restart network manager?"
14. "Where is the sources.list file located?"
15. "How to update Ubuntu from terminal?"
```

---

### 2. **AMBIGUOUS Queries** (Should trigger follow-up questions)

#### Too Vague
```
16. "Hello"
17. "Help me"
18. "Something is wrong"
19. "It's not working"
20. "Fix this"
```

#### Off-Topic
```
21. "What's the weather today?"
22. "How do I cook pasta?"
23. "Tell me a joke"
24. "What is the capital of France?"
25. "Recommend a good movie"
```

#### Multiple Unrelated Issues
```
26. "My WiFi doesn't work and also how do I bake a cake?"
27. "Fix my printer and tell me about Python programming"
```

---

### 3. **Edge Cases** (Test system robustness)

#### Partial Information
```
28. "Error message appeared"
29. "Installation failed"
30. "Can't login"
31. "Screen is black"
32. "Package manager issue"
```

#### Typos and Variations
```
33. "ubunto wifi problm"
34. "cant instal softwre"
35. "netwerk not wurking"
```

#### Complex Multi-Part Questions
```
36. "My Ubuntu system won't boot, I see a GRUB error, and I need to recover my files"
37. "WiFi connects but no internet, tried restarting router, what else can I do?"
38. "Installed new graphics driver, now screen resolution is wrong and system is slow"
```

---

### 4. **Retrieval Quality Tests** (Test context relevance)

#### High Similarity Expected
```
39. "wireless connection not working in ubuntu"
40. "how to repair broken packages in apt"
41. "ubuntu boot failure after system update"
42. "bluetooth device paired but no audio"
```

#### Low Similarity Expected (Should handle gracefully)
```
43. "How to configure Apache web server?"
44. "MySQL database connection timeout"
45. "Docker container networking issues"
46. "Kubernetes pod deployment failed"
```

---

### 5. **Hallucination Detection Tests** (Verify context-grounded responses)

#### Questions Where Context May Be Limited
```
47. "What are the exact steps to fix GRUB bootloader?"
48. "How do I configure advanced firewall rules?"
49. "What's the best way to optimize Ubuntu performance?"
50. "How to set up a VPN on Ubuntu?"
```

**Expected Behavior:** System should either:
- Provide answer based ONLY on retrieved context
- Say "I don't have specific information about that" if context is insufficient
- NOT make up commands or procedures

---

### 6. **Conversation Context Tests** (Test multi-turn dialogue)

#### Follow-up Questions
```
First: "My WiFi is not working"
Then: "I already tried restarting the router"
Then: "What about the network manager?"
Then: "How do I check if the driver is installed?"
```

#### Clarification Flow
```
First: "Something is broken"
System: [Should ask for clarification]
Then: "My WiFi connection"
System: [Should now provide WiFi help]
```

---

## 📊 Expected Results by Category

### Intent Classification
- **CLEAR queries (1-15, 28-44, 47-50):** Should proceed to retrieval and generation
- **AMBIGUOUS queries (16-27):** Should ask follow-up questions
- **Edge cases (28-32):** May be CLEAR or AMBIGUOUS depending on prompt tuning

### Retrieval Quality
- **High similarity (39-42):** Should retrieve relevant Ubuntu dialogue context
- **Low similarity (43-46):** Should have low similarity scores, may trigger fallback

### Hallucination Prevention
- **Queries 47-50:** Responses should NOT contain:
  - Commands not in the retrieved context
  - File paths not mentioned in context
  - Made-up version numbers or package names
  - Fabricated error messages

### Response Quality Indicators

✅ **Good Response:**
- References information from retrieved context
- Provides specific commands/steps from the knowledge base
- Acknowledges limitations when context is insufficient
- Stays focused on Ubuntu technical support

❌ **Poor Response (Hallucination):**
- Invents commands not in the context
- Makes up file paths or configuration details
- Provides generic advice not grounded in retrieved data
- Goes beyond what's in the knowledge base

---

## 🧪 Testing Workflow

### 1. Basic Functionality Test
```bash
# Start the chatbot
python chatbot.py

# Test queries 1-5 (basic CLEAR queries)
# Verify: No crashes, responses generated
```

### 2. Intent Classification Test
```bash
# Test queries 16-20 (AMBIGUOUS)
# Verify: System asks follow-up questions

# Test queries 1-5 (CLEAR)
# Verify: System proceeds to answer
```

### 3. Retrieval Quality Test
```bash
# Test queries 39-42 (high similarity expected)
# Check terminal logs for similarity scores
# Verify: Scores > 0.5

# Test queries 43-46 (low similarity expected)
# Verify: System handles gracefully (fallback message or limited answer)
```

### 4. Hallucination Detection Test
```bash
# Test queries 47-50
# Manually verify responses against retrieved context
# Check: Are commands/paths/details actually in the context?
```

### 5. Conversation Flow Test
```bash
# Test multi-turn conversations (section 6)
# Verify: System maintains context across turns
```

---

## 📝 Logging and Debugging

Monitor terminal output for:
```
chatbot_router          # Entry point
CLEAR/AMBIGUOUS         # Intent classification result
stream_response         # Response generation started
retrieve_context: Retrieved X docs, highest score: Y.YY  # Retrieval stats
```

---

## 🎯 Success Criteria

After testing, your system should:

1. ✅ **Not crash** on any query type
2. ✅ **Classify intent correctly** (>90% accuracy on CLEAR vs AMBIGUOUS)
3. ✅ **Retrieve relevant context** (similarity scores > 0.5 for relevant queries)
4. ✅ **Generate grounded responses** (no hallucinated commands/details)
5. ✅ **Handle edge cases gracefully** (fallback messages when appropriate)
6. ✅ **Maintain conversation context** (multi-turn dialogue works)

---

## 📈 Performance Comparison

Before and after improvements, track:

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Crash Rate | High | 0% | 0% |
| Intent Accuracy | Low | ? | >90% |
| Avg Similarity Score | Variable | ? | >0.6 |
| Hallucination Rate | 100% | ? | <20% |
| Faithfulness | 0.0 | ? | >0.8 |

---

## 🔍 Quick Test Script

Save this as `quick_test.py`:

```python
from retriever.vector_store import get_vectorstore
from retriever.retriever import retrieve_context

test_queries = [
    "My WiFi is not working",
    "Hello",
    "Ubuntu won't boot after update",
    "How to configure Apache?"
]

vectorstore = get_vectorstore()

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    context, score = retrieve_context(vectorstore, query)
    print(f"Similarity Score: {score:.4f}")
    print(f"Context Length: {len(context)} chars")
    print(f"Context Preview: {context[:200]}...")
```

Run with: `python quick_test.py`

---

## 💡 Tips for Testing

1. **Start with basic queries** (1-5) to verify system works
2. **Test intent classification** (16-27) to see CLEAR vs AMBIGUOUS detection
3. **Check terminal logs** for similarity scores and retrieval stats
4. **Manually verify responses** against the retrieved context shown in logs
5. **Test edge cases** (28-32) to see how system handles ambiguity
6. **Try conversation flows** (section 6) to test multi-turn dialogue

---

Good luck with testing! 🚀