import gradio as gr
import time
from context_expansion.intent_analyzer import analyze_intent

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator.generator_llm import generator_llm
from generator.prompt_builder import build_prompt
from retriever.retriever import retrieve_context
from retriever.vector_store import get_vectorstore

# def is_obviously_clear(query: str) -> bool:  # bypass Gatekeeper (analyze_intent). Its marking all query AMBIGUOUS
#     return len(query.split()) >= 4

def chatbot_router(message, history):

    # if is_obviously_clear(message):
    #     return stream_response(message, history)
    print("chatbot_router")
    intent = analyze_intent(message)
    
    if intent["status"] == "AMBIGUOUS":
        print("AMBIGUOUS")
        yield intent["follow_up_question"]
        return
    # if intent["status"] == "CLEAR":
    #     return stream_response(message, history)
    print("CLEAR")
    for chunk in stream_response(message, history):
        yield chunk

def stream_response(message, history):
    if not message:
        yield ""
        return

    print("stream_response")
    context, top_similarity_score = retrieve_context(get_vectorstore(), message)

    # if top_similarity_score < 0.3:
    #     return chatbot_router()

    prompt = build_prompt(
        user_question=message,
        context=context,
        history=history
    )

    response = generator_llm().generate_text(prompt)
    print(response)

    partial = ""
    for token in response.split():
        partial += token + " "
        time.sleep(0.015)
        yield partial

chatbot = gr.ChatInterface(
    fn=chatbot_router,
    textbox=gr.Textbox(
        container=False,
        scale=7
    )
)

chatbot.launch()