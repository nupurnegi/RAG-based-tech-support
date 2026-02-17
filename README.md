# RAG-Based Technical Support Assistant for Ubuntu

A Retrieval-Augmented Generation (RAG) system for Ubuntu technical support, powered by IBM watsonx.ai and Milvus vector database. This is a research prototype demonstrating RAG architecture with comprehensive evaluation metrics.

## 🎯 Overview

This system provides intelligent technical support for Ubuntu-related queries by:
- **Analyzing user intent** to determine query clarity (CLEAR vs AMBIGUOUS)
- **Retrieving relevant context** from Ubuntu dialogue dataset using semantic search
- **Generating accurate responses** grounded in retrieved context
- **Displaying confidence indicators** showing retrieval quality and system transparency
- **Tracking performance metrics** including faithfulness, relevance, and hallucination detection

## 🏗️ Architecture

```
User Query → Intent Analyzer → Retriever → Generator → Response with Confidence
                 ↓                  ↓           ↓              ↓
            CLEAR/AMBIGUOUS    Vector Search  watsonx.ai   Metadata Display
```

### Core Components

1. **Intent Analyzer** ([`context_expansion/`](context_expansion/)): 
   - Classifies queries as CLEAR or AMBIGUOUS
   - Requests clarification for ambiguous queries
   - Uses IBM watsonx Granite model

2. **Retriever** ([`retriever/`](retriever/)): 
   - Semantic search using Milvus vector database
   - Two-tier similarity thresholds (0.5 primary, 0.4 fallback)
   - Adaptive retrieval (k=8 initial, k=12 expanded)
   - Returns context with similarity scores

3. **Generator** ([`generator/`](generator/)): 
   - IBM watsonx Granite-13B-Chat-V2 model
   - Temperature: 0.1 (deterministic, factual responses)
   - Max tokens: 300 (complete answers)
   - Enhanced anti-hallucination prompts

4. **UI with Confidence Indicators** ([`ui/`](ui/)):
   - Gradio web interface
   - Color-coded confidence levels (🟢 High, 🟡 Medium, 🔴 Low)
   - Response metadata (similarity score, sources, disclaimer)
   - Async operations for responsive experience

5. **Evaluation Framework** ([`evaluation/`](evaluation/)): 
   - Context Relevance, Faithfulness, Hallucination Rate
   - Answer Relevance, Precision, Recall
   - Automated scoring with LLM judges

## 📊 Current Performance (V1 Configuration)

Based on evaluation with `scored_results_v1.json`:

| Metric | Score | Description |
|--------|-------|-------------|
| **Context Relevance** | 0.839 | Retrieved context relevance to query |
| **Faithfulness** | 0.103 | Response grounding in context |
| **Hallucination Rate** | 0.897 | Information not in context (89.7%) |
| **Answer Relevance** | 2.556 | How well answer addresses query |
| **Precision** | 0.088 | Accuracy of retrieved information |
| **Recall** | 0.697 | Coverage of relevant information |

**Note:** High hallucination rate is a documented limitation of LLM-based systems and represents a key research finding. See [`HALLUCINATION_ISSUE_EXPLAINED.md`](HALLUCINATION_ISSUE_EXPLAINED.md) for detailed analysis.

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
IBM watsonx.ai account
Milvus vector database instance
HuggingFace account
```

### Installation

```bash
# Clone repository
git clone <repository-url>
cd RAG-based-tech-support

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Update [`app/config.py`](app/config.py) with your credentials:

```python
WATSONX_CREDENTIALS = {
    "url": "your-watsonx-url",
    "apikey": "your-api-key"
}
PROJECT_ID = "your-project-id"
WATSONX_MODEL_ID = "ibm/granite-13b-chat-v2"
MILVUS_URL = "your-milvus-url"
MILVUS_TOKEN = "your-milvus-token"
HF_TOKEN = "your-huggingface-token"
```

### Data Preparation

```bash
# Load and preprocess Ubuntu dialogue dataset
python data_prep/data_loader.py

# Generate embeddings using sentence-transformers
python data_prep/data_embedding.py

# Insert into Milvus vector database
python data_prep/insert_data.py
```

### Run the Chatbot

```bash
python chatbot.py
```

The Gradio interface will launch at `http://localhost:7860`

## 📁 Project Structure

```
RAG-based-tech-support/
├── app/
│   └── config.py                    # Configuration and credentials
├── context_expansion/
│   ├── intent_analyzer.py           # Intent classification logic
│   ├── intent_llm.py                # LLM for intent analysis
│   └── intent_prompt.py             # Intent classification prompts
├── data_prep/
│   ├── data_loader.py               # Dataset loading and preprocessing
│   ├── data_embedding.py            # Generate embeddings
│   ├── insert_data.py               # Insert data into Milvus
│   └── store_data.py                # Data storage utilities
├── evaluation/
│   ├── run_generation.py            # Generate evaluation results
│   ├── run_generation_small.py      # Small dataset evaluation
│   ├── run_scoring.py               # Score generated responses
│   ├── run_scoring_small.py         # Small dataset scoring
│   ├── data/
│   │   ├── eval_queries.json        # Full evaluation queries
│   │   └── eval_queries_small.json  # Small evaluation set
│   ├── metrics/
│   │   ├── answer_relevance.py      # Answer relevance scoring
│   │   ├── context_relevance.py     # Context relevance scoring
│   │   ├── faithfulness.py          # Faithfulness measurement
│   │   └── precision_recall.py      # Precision/recall calculation
│   └── utils/
│       ├── claim_extractor.py       # Extract claims from responses
│       ├── llm_judge.py             # LLM-based evaluation
│       └── number_extractor.py      # Extract numeric scores
├── generator/
│   ├── generator_llm.py             # Response generation LLM
│   └── prompt_builder.py            # Prompt construction with anti-hallucination
├── retriever/
│   ├── retriever.py                 # Context retrieval with adaptive thresholds
│   └── vector_store.py              # Milvus vector store interface
├── ui/
│   ├── __init__.py                  # UI module exports
│   └── gradio_interface.py          # Gradio interface with confidence indicators
├── utils/
│   ├── __init__.py                  # Utils module exports
│   ├── constants.py                 # System constants and thresholds
│   └── helpers.py                   # Helper functions
├── archived_features/
│   └── v3_validation/               # V3 validation experiments (archived)
├── chatbot.py                       # Main chatbot application (async)
├── requirements.txt                 # Python dependencies
├── DEMO_PREPARATION_GUIDE.md        # Guide for successful demo
├── DISSERTATION_V1_JOURNEY.md       # Complete V1 development documentation
├── DISSERTATION_POST_V1_EXPLORATION.md  # V2/V3 experiments and analysis
├── HALLUCINATION_ISSUE_EXPLAINED.md # Detailed hallucination analysis
└── README.md                        # This file
```

## 🎨 Key Features

### 1. Visual Confidence Indicators

Every response includes:
- **Color-coded confidence level**: 🟢 High (≥0.7), 🟡 Medium (0.5-0.7), 🔴 Low (<0.5)
- **Similarity score**: Exact retrieval quality metric
- **Source count**: Number of documents used
- **Disclaimer**: Research prototype warning

### 2. Intent Classification

Automatically detects ambiguous queries and requests clarification:
- **CLEAR**: Proceeds with response generation
- **AMBIGUOUS**: Asks follow-up questions for clarification

### 3. Adaptive Retrieval

Two-tier retrieval strategy:
- **Primary**: k=8 documents, threshold=0.5
- **Fallback**: k=12 documents, threshold=0.4 (if <3 relevant docs found)

### 4. Async Operations

Non-blocking operations for responsive UI:
- Intent analysis runs in executor
- Context retrieval runs in executor
- Response generation runs in executor
- Immediate feedback: "🔍 Generating response..."

### 5. Conversation Memory

Maintains context across multi-turn conversations (last 3 turns)

## 🔧 Configuration Options

### Generator Settings ([`generator/generator_llm.py`](generator/generator_llm.py))

```python
params={
    "temperature": 0.1,              # Lower = more deterministic
    "max_new_tokens": 300,           # Maximum response length
    "top_p": 0.85,                   # Nucleus sampling
    "repetition_penalty": 1.1,       # Prevent repetition
    "stop_sequences": ["\n\nUser:", "Assistant:"]
}
```

### Retriever Settings ([`retriever/retriever.py`](retriever/retriever.py))

```python
k=8                                  # Initial retrieval count
expanded_k=12                        # Expanded retrieval count
primary_threshold=0.5                # Primary similarity threshold
fallback_threshold=0.4               # Fallback similarity threshold
min_relevant_docs=3                  # Trigger for expansion
```

### UI Settings ([`utils/constants.py`](utils/constants.py))

```python
HIGH_SIMILARITY_THRESHOLD = 0.5      # Minimum score for response generation
STREAMING_DELAY_SECONDS = 0.005      # Display delay (reduced for speed)
CHATBOT_HEIGHT = 600                 # Chat window height
SERVER_PORT = 7860                   # Gradio server port
```

### Embedding Model ([`app/config.py`](app/config.py))

```python
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # HuggingFace sentence-transformers
```

## 📈 Evaluation

### Run Evaluation Pipeline

```bash

# Full dataset
python evaluation/run_generation.py
python evaluation/run_scoring.py
```

### Results Files

- `evaluation/scored_results_v1.json` - V1 baseline scores
- `evaluation/scored_results_v2.json` - V2 scores

### Metrics Explained

| Metric | Range | Description |
|--------|-------|-------------|
| **Context Relevance** | 0-1 | How relevant retrieved context is to query |
| **Faithfulness** | 0-1 | Whether response is grounded in context |
| **Hallucination Rate** | 0-1 | Proportion of information not in context |
| **Answer Relevance** | 0-5 | How well answer addresses the query |
| **Precision** | 0-1 | Accuracy of information in response |
| **Recall** | 0-1 | Coverage of relevant information from context |

## 🎯 Research Findings

### Key Challenges Identified

1. **High Hallucination Rate (89.7%)**
   - LLMs generate information beyond retrieved context
   - Caused by training bias and prompt engineering limitations
   - Cannot be fully solved with prompt engineering alone

2. **Low Faithfulness (10.3%)**
   - Responses deviate from retrieved context
   - Related to hallucination problem
   - Requires constrained generation or fine-tuning

3. **Intent Classification Sensitivity**
   - Tendency to mark queries as AMBIGUOUS
   - Trade-off between clarity and user experience

### Improvement Attempts (Archived)

**V2 Experiment**: No context baseline
- Removed context to test pure LLM performance
- Result: Even worse hallucination, confirmed need for RAG

**V3.0 Validation**: Strict semantic similarity
- Post-generation validation layer
- Result: Too strict, rejected valid responses

**V3.1 Validation**: Balanced approach
- Semantic similarity with lower threshold
- Result: Better but still imperfect, added latency

See [`DISSERTATION_POST_V1_EXPLORATION.md`](DISSERTATION_POST_V1_EXPLORATION.md) for complete analysis.

## 🛠️ Technologies Used

- **IBM watsonx.ai**: Granite-13B-Chat-V2 for generation and intent analysis
- **Milvus**: Vector database for semantic search
- **HuggingFace**: Sentence-transformers for embeddings
- **Gradio**: Web interface with async support
- **Python 3.8+**: Core language with asyncio

## 📝 Dataset

Uses the [Ubuntu Dialogue QA dataset](https://huggingface.co/datasets/sedthh/ubuntu_dialogue_qa) from HuggingFace:
- Real Ubuntu technical support conversations
- Question-answer pairs from IRC channels
- Covers wide range of Ubuntu issues

---

**Version**: V1 (Current)  
**Last Updated**: 2026-02-17  
**Status**: Research Prototype with Documented Limitations
