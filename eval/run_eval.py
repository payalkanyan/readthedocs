"""Groundedness evaluation for the AWS S3 RAG chatbot.

Runs a test set through the RAG system and a no-retrieval baseline, then scores
each answer with an LLM-as-judge (Qwen2.5-7B-Instruct) for groundedness — whether
claims in the answer are supported by the retrieved context.

Outputs:
  eval/results.json  — per-query answers, chunks, and judge verdicts
  eval/summary.md    — the grounded-rate delta (baseline vs chunk-grounded RAG)

Usage:
  python eval/run_eval.py            # full test set
  python eval/run_eval.py --limit 3  # quick smoke test
  python eval/run_eval.py --delay 0  # no pause between calls
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag.rag_chain import get_llm, format_docs, retriever, prompt

EVAL_DIR = Path(__file__).resolve().parent
QUESTIONS_PATH = EVAL_DIR / "questions.json"
RESULTS_PATH = EVAL_DIR / "results.json"
SUMMARY_PATH = EVAL_DIR / "summary.md"

# Baseline: free-form answer with NO retrieved context (model uses parametric
# knowledge only). Lets the model answer freely so hallucinations are visible.
BASELINE_PROMPT = PromptTemplate.from_template(
    "Answer the following question concisely.\n\n"
    "Question: {question}\n"
    "Answer:"
)

# Judge: a claim is grounded if directly supported by the context; otherwise
# ungrounded. An "I don't know / not available" answer is grounded (no claims).
JUDGE_PROMPT = PromptTemplate.from_template(
    "You are an evaluator checking groundedness.\n"
    "A claim is GROUNDED if it is directly supported by the context below.\n"
    "A claim is UNGROUNDED if the answer states a fact, number, or detail not present in the context.\n"
    "An answer that says it does not know, or the answer is not available, is GROUNDED (no unsupported claims).\n\n"
    "Context:\n{context}\n\n"
    "Answer:\n{answer}\n\n"
    "Does the answer contain any claim NOT supported by the context?\n"
    "Reply with exactly one word on the first line: GROUNDED or UNGROUNDED.\n"
    "Then list any unsupported claims (or write 'none')."
)


def join_chunks(chunks):
    if not chunks:
        return "(no context provided)"
    return "\n\n".join(chunks)


def run_rag(question):
    """Full system: k=4 retrieval + grounding prompt. Returns (answer, chunks)."""
    docs = retriever.invoke(question)
    context = format_docs(docs)
    chain = prompt | get_llm() | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})
    return answer, [d.page_content for d in docs]


def run_baseline(question):
    """No-retrieval baseline. Returns (answer, [])."""
    chain = BASELINE_PROMPT | get_llm() | StrOutputParser()
    answer = chain.invoke({"question": question})
    return answer, []


def judge(context, answer):
    chain = JUDGE_PROMPT | get_llm() | StrOutputParser()
    verdict = chain.invoke({"context": context or "(no context provided)", "answer": answer})
    upper = verdict.upper()
    if "UNGROUNDED" in upper:
        label = "ungrounded"
    elif "GROUNDED" in upper:
        label = "grounded"
    else:
        label = "unknown"
    return label, verdict


def main():
    parser = argparse.ArgumentParser(description="Run groundedness eval")
    parser.add_argument("--limit", type=int, default=None, help="run only first N questions")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between HF calls")
    args = parser.parse_args()

    questions = json.loads(QUESTIONS_PATH.read_text())
    if args.limit:
        questions = questions[: args.limit]

    results = []
    rag_grounded = 0
    baseline_grounded = 0
    total = len(questions)

    for i, q in enumerate(questions, 1):
        question = q["question"]
        print(f"[{i}/{total}] {question}")

        rag_answer, chunks = run_rag(question)
        time.sleep(args.delay)
        rag_label, rag_verdict = judge(join_chunks(chunks), rag_answer)
        time.sleep(args.delay)

        baseline_answer, _ = run_baseline(question)
        time.sleep(args.delay)
        baseline_label, baseline_verdict = judge("", baseline_answer)
        time.sleep(args.delay)

        if rag_label == "grounded":
            rag_grounded += 1
        if baseline_label == "grounded":
            baseline_grounded += 1

        results.append({
            "id": q["id"],
            "question": question,
            "category": q["category"],
            "rag": {"answer": rag_answer, "retrieved_chunks": chunks, "label": rag_label, "judge": rag_verdict},
            "baseline": {"answer": baseline_answer, "label": baseline_label, "judge": baseline_verdict},
        })
        RESULTS_PATH.write_text(json.dumps(results, indent=2))
        print(f"    RAG: {rag_label} | baseline: {baseline_label}")

    rag_rate = round(100 * rag_grounded / total, 1)
    baseline_rate = round(100 * baseline_grounded / total, 1)

    summary = f"""# Groundedness Evaluation Summary

Test set: {total} questions
Judge: Qwen2.5-7B-Instruct (LLM-as-judge)

## Results

| System | Fully grounded |
|--------|---------------:|
| Baseline (no retrieval) | {baseline_rate}% |
| RAG (chunk-grounded, k=4) | {rag_rate}% |

## Delta

Grounded rate: baseline {baseline_rate}% -> chunk-grounded {rag_rate}%

> Evaluated groundedness on a {total}-query test set, grounding answers in
> retrieved source chunks: baseline {baseline_rate}% -> RAG {rag_rate}% fully
> grounded.
"""
    SUMMARY_PATH.write_text(summary)
    print("\n" + summary)


if __name__ == "__main__":
    main()
