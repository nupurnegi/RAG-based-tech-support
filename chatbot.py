"""
Main chatbot application with built-in latency measurement.

"""

import os
import sys
import asyncio
import time
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from context_expansion.intent_analyzer import analyze_intent
from generator.generator_llm import generator_llm
from generator.prompt_builder import build_prompt
from retriever.retriever import retrieve_context
from retriever.vector_store import get_vectorstore
from utils.constants import HIGH_SIMILARITY_THRESHOLD
from utils.helpers import validate_query
from ui import create_demo, launch_interface

# Enable/disable timing measurements (set to False to disable)
ENABLE_TIMING = True

# Timing log file path
TIMING_LOG_FILE = "timing/timing_log.json"


def log_timing_data(timing_data):
    """
    Append timing data to log file.
    
    Args:
        timing_data (dict): Dictionary containing timing information
    """
    if not ENABLE_TIMING:
        return
    
    try:
        # Read existing data
        if os.path.exists(TIMING_LOG_FILE):
            with open(TIMING_LOG_FILE, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Append new data
        logs.append(timing_data)
        
        # Write back to file
        with open(TIMING_LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"✅ Timing data logged to {TIMING_LOG_FILE}")
    
    except Exception as e:
        print(f"⚠️  Failed to log timing data: {e}")


async def chatbot_router(message, history):
    """
    Route user messages through intent analysis before generating responses.
    
    1. Analyzes query intent (CLEAR vs AMBIGUOUS)
    2. Returns follow-up question if AMBIGUOUS
    3. Generates response if CLEAR
    
    Args:
        message (str): User's input message
        history (list): Conversation history
        
    Yields:
        str: Response for streaming display
    """
    total_start = time.time() if ENABLE_TIMING else None
    intent_start = None
    intent_time = 0.0
    
    if ENABLE_TIMING:
        print("\n" + "⏱️ "*40)
        print("TIMING MEASUREMENT ENABLED")
        print("⏱️ "*40)
    
    print("chatbot_router - Processing message")
    
    # Analyze intent (run in executor to not block)
    if ENABLE_TIMING:
        intent_start = time.time()
    
    loop = asyncio.get_event_loop()
    intent = await loop.run_in_executor(None, analyze_intent, message)
    
    if ENABLE_TIMING and intent_start is not None:
        intent_time = time.time() - intent_start
        print(f"⏱️  Intent Analysis: {intent_time:.3f}s")
    
    # Handle AMBIGUOUS queries
    if intent["status"] == "AMBIGUOUS":
        print("AMBIGUOUS - Requesting clarification (NO RETRIEVAL/GENERATION)")
        
        if ENABLE_TIMING and total_start is not None:
            total_time = time.time() - total_start
            print(f"\n{'='*80}")
            print("⏱️  LATENCY BREAKDOWN (AMBIGUOUS QUERY):")
            print(f"{'='*80}")
            print(f"  Intent Analysis:     {intent_time:.3f}s (100%)")
            print(f"  Vector Retrieval:    0.000s (skipped)")
            print(f"  Response Generation: 0.000s (skipped)")
            print(f"  ─────────────────────────────")
            print(f"  ⏱️  TOTAL:            {total_time:.3f}s")
            print(f"{'='*80}\n")
            
            # Log timing data
            timing_data = {
                "timestamp": datetime.now().isoformat(),
                "query": message,
                "status": "AMBIGUOUS",
                "intent_time": round(intent_time, 3),
                "retrieval_time": 0.0,
                "generation_time": 0.0,
                "total_time": round(total_time, 3),
                "similarity_score": None,
                "confidence_level": None
            }
            log_timing_data(timing_data)
        
        yield intent["follow_up_question"]
        return
    
    # Handle CLEAR queries
    print("CLEAR - Generating response")
    async for chunk in stream_response(message, history, total_start, intent_time):
        yield chunk


async def stream_response(message, history, total_start=None, intent_time=0.0):
    """
    Generate and stream response for a user query.
    
    This function:
    1. Retrieves relevant context from vector store
    2. Checks similarity threshold
    3. Builds prompt with context and history
    4. Generates response using LLM
    5. Streams response word by word
    
    Args:
        message (str): User's input message
        history (list): Conversation history
        total_start (float, optional): Start time for total latency measurement
        intent_time (float, optional): Time taken for intent analysis
        
    Yields:
        str: Response chunks for streaming display
    """
    # Validate input
    if not validate_query(message):
        yield ""
        return

    print("\n" + "="*80)
    print("STREAM RESPONSE - Starting generation")
    print("="*80)
    
    # Yield immediately to show we're processing
    yield "🔍 Generating response..."
    
    # Get event loop for async operations
    loop = asyncio.get_event_loop()
    
    # Retrieve relevant context (run in executor to not block)
    retrieval_start = time.time() if ENABLE_TIMING else None
    
    context, top_similarity_score = await loop.run_in_executor(
        None, retrieve_context, get_vectorstore(), message
    )
    
    retrieval_time = 0.0
    if ENABLE_TIMING and retrieval_start is not None:
        retrieval_time = time.time() - retrieval_start
        print(f"⏱️  Vector Retrieval: {retrieval_time:.3f}s")
    
    print(f"\nSimilarity Score: {top_similarity_score:.4f}")
    
    # Determine confidence level based on similarity score
    if top_similarity_score >= 0.7:
        confidence_indicator = "🟢 **High Confidence**"
        confidence_level = "High"
        confidence_text = "Found highly relevant information"
    elif top_similarity_score >= 0.5:
        confidence_indicator = "🟡 **Medium Confidence**"
        confidence_level = "Medium"
        confidence_text = "Found related information"
    else:
        confidence_indicator = "🔴 **Low Confidence**"
        confidence_level = "Low"
        confidence_text = "Limited relevant information available"
    
    # Check if retrieval quality is sufficient
    if top_similarity_score < HIGH_SIMILARITY_THRESHOLD:
        fallback_msg = (
            f"{confidence_indicator} (Score: {top_similarity_score:.2f})\n\n"
            f"_{confidence_text}_\n\n"
            "I couldn't find highly relevant information for your query. "
            "Could you provide more details about your Ubuntu issue?"
        )
        print(f"Low similarity - returning fallback message")
        yield fallback_msg
        return
    
    # Build prompt with context and history
    prompt = build_prompt(
        user_question=message,
        context=context,
        history=history
    )

    # Generate response (run in executor to not block)
    generation_start = time.time() if ENABLE_TIMING else None
    
    response = await loop.run_in_executor(
        None, generator_llm().generate_text, prompt
    )
    
    generation_time = 0.0
    if ENABLE_TIMING and generation_start is not None:
        generation_time = time.time() - generation_start
        print(f"⏱️  Response Generation: {generation_time:.3f}s")
    
    print("\n" + "="*80)
    print("GENERATED RESPONSE:")
    print("="*80)
    print(response)
    print("="*80 + "\n")

    # Count number of context sources
    num_sources = len([c for c in context.split('\n\n') if c.strip()])
    
    # Print timing summary and log data
    if ENABLE_TIMING and total_start is not None:
        total_time = time.time() - total_start
        print(f"\n{'='*80}")
        print("⏱️  LATENCY BREAKDOWN (CLEAR QUERY):")
        print(f"{'='*80}")
        print(f"  Intent Analysis:     {intent_time:.3f}s ({intent_time/total_time*100:.1f}%)")
        print(f"  Vector Retrieval:    {retrieval_time:.3f}s ({retrieval_time/total_time*100:.1f}%)")
        print(f"  Response Generation: {generation_time:.3f}s ({generation_time/total_time*100:.1f}%)")
        print(f"  ─────────────────────────────")
        print(f"  ⏱️  TOTAL:            {total_time:.3f}s")
        print(f"{'='*80}\n")
        
        # Log timing data
        timing_data = {
            "timestamp": datetime.now().isoformat(),
            "query": message,
            "status": "CLEAR",
            "intent_time": round(intent_time, 3),
            "retrieval_time": round(retrieval_time, 3),
            "generation_time": round(generation_time, 3),
            "total_time": round(total_time, 3),
            "similarity_score": round(top_similarity_score, 4),
            "confidence_level": confidence_level,
            "num_sources": num_sources
        }
        log_timing_data(timing_data)
    
    # Build response with confidence indicator and metadata
    full_response = (
        f"{confidence_indicator} (Score: {top_similarity_score:.2f})\n\n"
        f"_{confidence_text}_\n\n"
        f"{response}\n\n"
        f"---\n"
        f"📊 **Response Metadata:**\n"
        f"- Similarity Score: {top_similarity_score:.3f}\n"
        f"- Sources Retrieved: {num_sources}\n"
        f"- Confidence Level: {confidence_level}\n\n"
        f"_⚠️ Please verify commands before execution. This is a research prototype._"
    )

    # Yield complete response immediately
    yield full_response


if __name__ == "__main__":
    # Create and launch the interface
    demo = create_demo(chatbot_router)
    launch_interface(demo, share=False, show_error=True)
