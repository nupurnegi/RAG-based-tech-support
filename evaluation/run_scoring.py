import json
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evaluation.metrics.context_relevance import context_relevance
from evaluation.metrics.faithfulness import faithfulness
from evaluation.metrics.answer_relevance import answer_relevance
from evaluation.metrics.precision_recall import precision_recall

if __name__ == "__main__":
    with open("evaluation/results1.json") as f:
        results_short1 = json.load(f)

    scored_results = []

    for item in results_short1:
        print(item["id"])
        query = item["query"]
        context = item["context"]
        answer = item["answer"]

        metrics = {}
        print("Running context_relevance")
        metrics["context_relevance"] = context_relevance(query, context).splitlines()[0].strip()
        print("Running faithfulness")
        metrics["faithfulness"] = faithfulness(query, context)
        print("Running hallucination_rate")
        metrics["hallucination_rate"] = 1 - metrics["faithfulness"]
        print("Running answer_relevance")
        metrics["answer_relevance"] = answer_relevance(query, answer).splitlines()[0].strip()
        print(metrics["answer_relevance"])
        print("Running precision & recall")
        recall, precision = precision_recall(context, answer)
        print("done precision and recall")
        metrics["precision"] = precision
        metrics["recall"] = recall

        print("metrics: ", metrics)

        scored_results.append({
            **item,
            "metrics": metrics
        })

    with open("evaluation/scored_results.json", "w") as f:
        json.dump(scored_results, f, indent=2)

    print("Saved evaluation/scored_results.json")
