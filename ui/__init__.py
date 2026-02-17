"""
User interface module for the RAG-based Technical Support Assistant.

This package contains:
- gradio_interface: Gradio UI components and configuration
"""

from ui.gradio_interface import (
    create_demo,
    launch_interface,
    get_example_queries,
)

__all__ = [
    'create_demo',
    'launch_interface',
    'get_example_queries',
]

 
