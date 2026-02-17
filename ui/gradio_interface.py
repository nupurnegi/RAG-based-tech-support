"""
Gradio user interface module for the chatbot.

This module handles:
- UI layout and styling
- Component configuration
- Example queries
- Tips and documentation display
"""

import gradio as gr
from utils.constants import (
    CHATBOT_HEIGHT,
    TEXTBOX_INITIAL_LINES,
    TEXTBOX_MAX_LINES,
    SERVER_PORT,
)


def create_header():
    """
    Create the header section of the UI.
    
    Returns:
        gr.Markdown: Header markdown component
    """
    return gr.Markdown(
        """
        # 🐧 Ubuntu Technical Support Assistant
        
        **Powered by RAG (Retrieval-Augmented Generation)**
        
        Ask me anything about Ubuntu technical issues, and I'll help you find solutions based on real support conversations.
        
        ---
        """
    )


def create_footer():
    """
    Create the footer section with tips and features.
    
    Returns:
        gr.Markdown: Footer markdown component
    """
    return gr.Markdown(
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


def get_example_queries():
    """
    Get list of example queries for the chatbot.
    
    Returns:
        list: List of example query strings
    """
    return [
        "My WiFi is not connecting",
        "Ubuntu won't boot after update",
        "How do I fix broken packages?",
        "Bluetooth device paired but no sound",
        "Getting disk space low warning",
    ]


def create_chatbot_interface(chatbot_fn):
    """
    Create the main chat interface component.
    
    Args:
        chatbot_fn: Function to handle chat messages
        
    Returns:
        gr.ChatInterface: Configured chat interface
    """
    return gr.ChatInterface(
        fn=chatbot_fn,
        chatbot=gr.Chatbot(
            height=CHATBOT_HEIGHT,
            show_label=False,
            avatar_images=(None, "🤖"),
            render_markdown=True,
        ),
        textbox=gr.Textbox(
            placeholder="Describe your Ubuntu issue here... (e.g., 'My WiFi is not connecting')",
            container=False,
            scale=7,
            lines=TEXTBOX_INITIAL_LINES,
            max_lines=TEXTBOX_MAX_LINES,
            show_label=False,
        ),
        submit_btn=True,
        examples=get_example_queries(),
        concurrency_limit=None,  # Remove concurrency limit for faster responses
    )


def create_demo(chatbot_fn):
    """
    Create the complete Gradio demo interface.
    
    Args:
        chatbot_fn: Function to handle chat messages
        
    Returns:
        gr.Blocks: Complete Gradio interface
    """
    with gr.Blocks(title="Ubuntu Technical Support Assistant") as demo:
        create_header()
        create_chatbot_interface(chatbot_fn)
        create_footer()
    
    return demo


def launch_interface(demo, share=False, show_error=True):
    """
    Launch the Gradio interface.
    
    Args:
        demo: Gradio Blocks interface
        share (bool): Whether to create public link
        show_error (bool): Whether to display errors in UI
    """
    demo.launch(
        server_name="0.0.0.0",
        server_port=SERVER_PORT,
        share=share,
        show_error=show_error,
    )

 
