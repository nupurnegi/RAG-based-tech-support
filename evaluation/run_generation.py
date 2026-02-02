import json
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retriever.vector_store import get_vectorstore
from retriever.retriever import retrieve_context
from generator.prompt_builder import build_prompt
from generator.generator_llm import generator_llm

from evaluation.metrics.context_relevance import context_relevance
from evaluation.metrics.faithfulness import faithfulness
from evaluation.metrics.answer_relevance import answer_relevance
from evaluation.metrics.precision_recall import precision_recall


def run_rag(query):
    vectorstore = get_vectorstore()

    context, similarity = retrieve_context(vectorstore, query)

    prompt = build_prompt(
        user_question=query,
        context=context,
        history=[]
    )

    answer = generator_llm().generate_text(prompt)

    return {
        "query": query,
        "context": context,
        "answer": answer,
        "similarity": similarity
    }

if __name__ == "__main__":
    with open("evaluation/data/eval_queries.json") as f:
        queries = json.load(f)

    results = []

    for item in queries:
        output = run_rag(item["query"])
        results.append({
            "id": item["id"],
            **output
        })

    with open("evaluation/results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Saved evaluation/results.json")
