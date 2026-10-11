# Evaluation Playbook — AI System Quality Assurance

## The Evaluation Stack

```
Production Metrics (online, real users)
    ↑ validates
Offline Evals (golden set, automated)
    ↑ gates
Unit Tests (specific behaviors, deterministic)
```

All three layers are required in a mature AI system.

---

## Building a Golden Test Set

1. **Collect real queries** — from user logs, support tickets, stakeholder requests
2. **Ensure diversity** — easy/hard, short/long, edge cases, adversarial
3. **Write reference answers** — human-authored ideal responses
4. **Annotate difficulty** — easy (must pass), hard (aspirational)
5. **Lock the set** — don't update it; create a new set for each major version

Minimum viable: 50 examples. Production: 200-500+.

---

## LLM-as-Judge

Use a separate, stronger LLM to evaluate outputs. Provide a rubric:

```python
JUDGE_PROMPT = """
You are evaluating an AI assistant's response.

Question: {question}
Reference Answer: {reference}
Model Response: {response}

Score the response on these dimensions (1-5 each):
- Accuracy: Is the information correct?
- Completeness: Does it address all parts of the question?  
- Conciseness: Is it appropriately brief without being incomplete?
- Groundedness: Are claims supported by evidence/context provided?

Respond ONLY with JSON: {"accuracy": N, "completeness": N, "conciseness": N, "groundedness": N, "overall": N, "reasoning": "..."}
"""
```

**Anti-pattern**: don't use the same model family to judge outputs it generated — use a different provider.

---

## G-Eval Framework

For open-ended evaluation:
1. Define evaluation criteria in natural language
2. Generate evaluation steps (chain-of-thought)
3. Score using form-filling approach
4. Average scores across multiple runs (temperature > 0)

---

## Hallucination Detection

### RAG hallucination
Check if claims in the response are entailed by retrieved context:
```
For each factual claim in the response:
  Is this claim supported by the provided context? [YES / NO / PARTIALLY]
  
Hallucination rate = # NO claims / total claims
```

### Open-domain hallucination
Use web search to fact-check specific claims. Flag any claim that:
- Contradicts a search result
- Cannot be found via search (invented facts)
- Contains suspiciously specific numbers/dates

---

## A/B Testing AI Systems

1. **Shadow mode**: new model runs alongside old, outputs compared but not shown to users
2. **Traffic split**: 10% of users get new model, compare downstream metrics
3. **Human preference**: show two outputs blind, ask which is better
4. **Metric gates**: must win on primary metric, not regress on secondary

Statistical significance: need ~1000 comparisons per variant minimum.

---

## Continuous Eval in CI/CD

```yaml
# .github/workflows/eval.yml
on: [push]
jobs:
  eval:
    steps:
      - run: python evals/run_golden_set.py --model $NEW_MODEL
      - run: python evals/compare_baseline.py --threshold 0.95
      # Fail if new model scores < 95% of baseline on golden set
```

Gate deploys on eval regressions. Never ship a regression to production.

---

## Metric Reference

| Task | Primary Metric | Secondary |
|---|---|---|
| QA / RAG | Answer Faithfulness, EM | Latency, context recall |
| Summarization | ROUGE-L, faithfulness | Length, factuality |
| Code generation | Pass@1, Pass@5 | Compilation rate |
| Classification | F1, Accuracy | Calibration |
| Dialogue | User satisfaction | Session length |
| Agents | Task completion | Step efficiency, cost |
