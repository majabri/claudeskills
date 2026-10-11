# Agents Deep Dive — Production Agentic Systems

## Agent Anatomy

Every agent has:
1. **Perception** — receives inputs (text, tool results, observations)
2. **Memory** — short-term (context window), long-term (vector store), working (scratchpad)
3. **Reasoning** — LLM that decides what to do next
4. **Action** — tool calls, sub-agent delegation, final response

---

## ReAct Pattern (Reasoning + Acting)

The most reliable single-agent loop:
```
Thought: I need to find the current price of AAPL stock.
Action: web_search("AAPL stock price today")
Observation: AAPL is trading at $189.45.
Thought: I now have the price, I can answer the user.
Final Answer: Apple stock is currently $189.45.
```

**Prompt template**:
```
You are an agent with access to tools.
For each step, output:
Thought: <your reasoning>
Action: <tool_name>(<params>)
Observation: <tool result - filled by system>
... repeat until done ...
Final Answer: <your response>
```

---

## Plan-and-Execute Pattern

Better for complex, multi-step tasks:
1. **Planner** (strong LLM): Given goal → produce ordered plan of steps
2. **Executor** (fast LLM + tools): Execute each step, return result
3. **Replanner** (optional): After each step, check if plan needs updating

Use when: tasks have >5 steps, steps are parallelizable, or early steps inform later ones.

---

## Multi-Agent Architecture

```
Supervisor Agent
├── Research Agent (tools: search, fetch)
├── Analysis Agent (tools: code_exec, calculator)
├── Writing Agent (tools: draft, format)
└── Critic Agent (tools: review, score)
```

**Communication**: agents pass structured messages:
```json
{
  "from": "research_agent",
  "to": "analysis_agent",
  "content": "Found 3 relevant papers...",
  "attachments": [...],
  "metadata": {"confidence": 0.85}
}
```

**Supervisor patterns**:
- **Sequential**: A → B → C (simple, predictable)
- **Parallel fan-out**: Supervisor → [A, B, C simultaneously] → merge
- **Dynamic routing**: Supervisor decides next agent based on result
- **Debate**: Two agents argue opposing views, supervisor decides

---

## Memory Systems

### Short-Term (In-Context)
- Everything in the current context window
- Limit: model's context length
- Strategy: summarize old turns when approaching limit

### Long-Term (Vector Store)
- Persist important facts, user preferences, past interactions
- Store: `{content, embedding, timestamp, metadata}`
- Retrieve on each new turn: top-k relevant memories

### Episodic (Session Summaries)
- At end of session, summarize key outcomes
- Store summaries indexed by date/topic
- Retrieve for future sessions with same user

---

## Tool Design Principles

```python
@tool
def search_web(query: str) -> str:
    """
    Search the web for current information.
    Use when: you need real-time data, recent events, or facts you're unsure about.
    Returns: top 3 search results as formatted text.
    """
    # atomic, single-purpose, clear error messages
    try:
        results = search_api.search(query)
        return format_results(results)
    except Exception as e:
        return f"Search failed: {str(e)}. Try a different query."
```

Rules for good tools:
- Single responsibility
- Clear docstring telling the agent WHEN to use it
- Explicit error messages (not silent failures)
- Return structured data when possible
- Idempotent where possible

---

## Common Failure Modes & Fixes

| Failure | Cause | Fix |
|---|---|---|
| Infinite loops | No termination condition | Max iterations + force-stop |
| Tool hallucination | LLM invents tool args | Strict tool schemas + validation |
| Context overflow | Long tasks exhaust window | Summarize intermediate results |
| Cascading errors | One bad step poisons rest | Checkpoint + retry with correction |
| Overconfident final answer | No verification step | Add critic agent or self-check |
| Slow execution | Sequential tool calls | Parallelize independent steps |

---

## Evaluation for Agents

- **Task completion rate**: % of goals fully achieved
- **Step efficiency**: steps taken vs optimal (human) baseline  
- **Tool call accuracy**: correct tool + correct args
- **Hallucination rate**: facts invented vs grounded
- **Cost per task**: tokens spent per completed goal

Use human evaluation for a random 5% sample; LLM-as-judge for scale.
