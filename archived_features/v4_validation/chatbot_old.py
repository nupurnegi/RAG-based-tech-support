"""
Main chatbot application using Gradio interface.

This module handles:
- User interface with Gradio
- Intent-based routing
- Response generation and streaming
- Conversation management
"""

import os
import sys
import time
import gradio as gr

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from context_expansion.intent_analyzer import analyze_intent
from generator.generator_llm import generator_llm
from generator.prompt_builder import build_prompt
from retriever.retriever import retrieve_context
from retriever.vector_store import get_vectorstore


# Configuration constants
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score for retrieval
STREAMING_DELAY = 0.015     # Delay between tokens for streaming effect


def chatbot_router(message, history):
    """
    Route user messages through intent analysis before generating responses.
    
    This function:
    1. Analyzes query intent (CLEAR vs AMBIGUOUS)
    2. Returns follow-up question if AMBIGUOUS
    3. Generates response if CLEAR
    
    Args:
        message (str): User's input message
        history (list): Conversation history
        
    Yields:
        str: Response chunks for streaming display
    """
    print("chatbot_router - Processing message")
    
    # Analyze intent
    intent = analyze_intent(message)
    
    # Handle AMBIGUOUS queries
    if intent["status"] == "AMBIGUOUS":
        print("AMBIGUOUS - Requesting clarification")
        yield intent["follow_up_question"]
        return
    
    # Handle CLEAR queries
    print("CLEAR - Generating response")
    for chunk in stream_response(message, history):
        yield chunk


def stream_response(message, history):
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
        
    Yields:
        str: Response chunks for streaming display
    """
    # Validate input
    if not message:
        yield ""
        return

    print("\n" + "="*80)
    print("STREAM RESPONSE - Starting generation")
    print("="*80)
    
    # Retrieve relevant context
    context, top_similarity_score = retrieve_context(get_vectorstore(), message)
    print(f"\nSimilarity Score: {top_similarity_score:.4f}")
    
    # Check if retrieval quality is sufficient
    if top_similarity_score < SIMILARITY_THRESHOLD:
        fallback_msg = (
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

    # Generate response
    response = generator_llm().generate_text(prompt)
    
    print("\n" + "="*80)
    print("GENERATED RESPONSE:")
    print("="*80)
    print(response)
    print("="*80 + "\n")

    # Stream response word by word
    partial = ""
    words = response.split()
    
    for i, word in enumerate(words):
        partial += word
        
        # Add space after word (except for last word)
        if i < len(words) - 1:
            partial += " "
        
        time.sleep(STREAMING_DELAY)
        yield partial
    
    # Ensure final response is complete
    yield response

# ============================================================================
# GRADIO USER INTERFACE
# ============================================================================

# Create enhanced UI with custom layout
with gr.Blocks(title="Ubuntu Technical Support Assistant") as demo:
    
    # Header section
    gr.Markdown(
        """
        # 🐧 Ubuntu Technical Support Assistant
        
        **Powered by RAG (Retrieval-Augmented Generation)**
        
        Ask me anything about Ubuntu technical issues, and I'll help you find solutions based on real support conversations.
        
        ---
        """
    )
    
    # Main chat interface
    chatbot_interface = gr.ChatInterface(
        fn=chatbot_router,
        chatbot=gr.Chatbot(
            height=600,                          # Large chat window
            show_label=False,                    # Hide label for cleaner look
            avatar_images=(None, "🤖"),          # Robot avatar for assistant
        ),
        textbox=gr.Textbox(
            placeholder="Describe your Ubuntu issue here... (e.g., 'My WiFi is not connecting')",
            container=False,                     # No container border
            scale=7,                             # Relative width
            lines=2,                             # Initial height
            max_lines=5,                         # Maximum height
            show_label=False,                    # Hide label
        ),
        submit_btn=True,                         # Enable submit button
        examples=[                               # Example queries
            "My WiFi is not connecting",
            "Ubuntu won't boot after update",
            "How do I fix broken packages?",
            "Bluetooth device paired but no sound",
            "Getting disk space low warning",
        ],
    )
    
    # Footer section with tips and features
    gr.Markdown(
        """
        ---
        
        ### 💡 Tips for Better Results:
        - Be specific about your Ubuntu issue
        - Mention error messages if you have them
        - Describe what you've already tried
        
        ### ⚙️ System Features:
        - **Intent Analysis**: Automatically detects if your query needs clarification
        - **Context Retrieval**: Searches through Ubuntu support conversations
        - **Grounded Responses**: Answers based only on retrieved knowledge
        """
    )

# Launch the application
demo.launch(
    server_name="0.0.0.0",    # Listen on all network interfaces
    server_port=7860,          # Default Gradio port
    share=False,               # Don't create public link
    show_error=True,           # Display errors in UI
)