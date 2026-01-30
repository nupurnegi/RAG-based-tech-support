import gradio as gr
import time
from context_expansion.intent_analyzer import analyze_intent

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator.generator_llm import load_llm
from generator.prompt_builder import build_prompt
from retriever.retriever import retrieve_context
from retriever.vector_store import get_vectorstore

def stream_response(message, history):
    if not message:
        return ""
    
    intent = analyze_intent(message) 
    
    # follow_up = ""
    # if intent["status"] == "AMBIGUOUS":
    #     # response = intent["follow_up_question"][0]
    #     follow_up = intent.get("follow_up_question")
    #     yield follow_up
    #     return
    if intent["status"] == "AMBIGUOUS":
        return intent["follow_up_question"][0]


    context = retrieve_context(get_vectorstore(), message)

    prompt = build_prompt(
        user_question=message,
        context=context,
        history=history
    )

    response = load_llm().generate_text(prompt)

    partial = ""
    for token in response.split():
        partial += token + " "
        time.sleep(0.015)
        yield partial

chatbot = gr.ChatInterface(
    fn=stream_response,
    textbox=gr.Textbox(
        container=False,
        scale=7
    )
)

chatbot.launch()