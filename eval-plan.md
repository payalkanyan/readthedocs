# Evaluation Plan — Kora (AWS Docs RAG Chatbot)

Goal: get one real, defensible number showing your chunk-grounded retrieval actually reduces hallucinations — enough to justify a resume line like "Reduced ungrounded claims by X% via chunk-grounded retrieval."

---

## 1. Build a small test set (30–45 min)

- Pick **20–30 questions** a real user would ask about the AWS docs you ingested (mix of simple factual lookups and more complex multi-part questions).
- Run each through Kora and save: `query, retrieved_chunks, generated_answer`.

## 2. Define "grounded" vs "ungrounded" (10 min)

A claim in the answer is **grounded** if it's directly supported by content in the retrieved chunks. It's **ungrounded/hallucinated** if the model added a fact, number, or detail not present in any retrieved chunk.

## 3. Score groundedness — two options, pick based on time available

**Option A — Manual scoring (most reliable, ~45–60 min for 20-30 queries):**
- For each answer, read it against its retrieved chunks.
- Mark each answer as `grounded` / `partially grounded` / `ungrounded`.
- Compute: `% fully grounded = grounded_count / total_queries`.

**Option B — LLM-as-judge (faster, good enough for a resume-level metric):**
- Write a short prompt: *"Given this retrieved context and this generated answer, does the answer contain any claims NOT supported by the context? Answer YES/NO and list unsupported claims."*
- Run this judge prompt (via the same Claude/Gemini API you're already using in the project) over all 20–30 answer/context pairs.
- Compute the same `% fully grounded` metric.

```python
groundedness_prompt = """
Context: {retrieved_chunks}
Answer: {generated_answer}

Does the answer contain any claim NOT supported by the context above?
Reply with: GROUNDED or UNGROUNDED, then list any unsupported claims.
"""
```

## 4. Build a naive baseline for comparison (20–30 min)

To claim you *reduced* hallucinations, you need something to compare against:

- **Baseline:** Run the same 20–30 queries with retrieval turned off, or with only top-1 chunk (no reranking/multi-chunk grounding) — i.e., a weaker retrieval setup.
- Score groundedness the same way (Option A or B) on this baseline set.

## 5. Compare and write down the delta

- `Grounded rate: baseline X% → chunk-grounded Y%`
- This is your real number. Even something like "58% → 84%" is far more credible than an unmeasured "significantly reduced."

## 6. Optional: retrieval precision as a secondary metric

- Of the chunks retrieved per query, what fraction were actually relevant/used in the final answer? Quick manual tag (relevant/not) on the same test set gives you a second number if you want it: `retrieval precision = relevant_chunks / total_retrieved`.

## 7. Turn it into the resume line

Once you have real numbers:
> "Evaluated groundedness on a 20-query test set, reducing unsupported claims from X% to Y% via chunk-grounded retrieval vs. a no-retrieval baseline"

If you don't get to this and need to ship the resume now — use the safe, honest fallback line instead:
> "Implemented chunk-grounded retrieval to reduce ungrounded model responses, validated via manual review of generated answers against source chunks"

No fabricated percentage, still shows evaluation thinking.
