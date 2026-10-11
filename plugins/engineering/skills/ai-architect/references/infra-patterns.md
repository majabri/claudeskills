# Infrastructure Patterns — Deploying AI Systems to Production

## AI API Service Architecture

```
                    ┌─────────────────────────────────┐
                    │           API Gateway           │
                    │   (rate limiting, auth, TLS)    │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │         AI Router Layer         │
                    │  (semantic cache + model select) │
                    └──────┬──────────────┬───────────┘
                           │              │
              ┌────────────▼──┐     ┌─────▼──────────┐
              │  LLM Provider │     │  RAG Pipeline  │
              │ (Anthropic /  │     │  (retrieve +   │
              │  OpenAI /...  │     │   rerank)      │
              └────────────┬──┘     └─────┬──────────┘
                           │              │
                    ┌──────▼──────────────▼───────────┐
                    │       Response Assembly          │
                    │   (streaming, citations,         │
                    │    guardrails, logging)          │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │         Observability           │
                    │  (traces, metrics, alerts)      │
                    └─────────────────────────────────┘
```

---

## Semantic Caching

Cache LLM responses by semantic similarity — not exact match:

```python
from gptcache import cache
from gptcache.embedding import Onnx

cache.init(
    embedding_func=Onnx().to_embeddings,
    similarity_evaluation=SearchDistanceEvaluation(),
)

# Automatically caches + retrieves similar queries
response = openai.chat.completions.create(model="gpt-4o", messages=[...])
```

Cache hit rates: typically 20-40% for customer support, lower for creative tasks.
TTL: match to data freshness requirements (1hr for news, 30 days for docs).

---

## Streaming Responses (SSE)

For good UX, always stream long-form AI responses:

```python
# FastAPI streaming endpoint
from fastapi.responses import StreamingResponse

async def stream_ai_response(query: str):
    async def generate():
        async with anthropic.messages.stream(
            model="claude-sonnet-4-20250514",
            messages=[{"role": "user", "content": query}]
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## Async Job Queue for Long Tasks

For tasks taking >10 seconds, use a job queue pattern:

```
Client → POST /jobs → {job_id: "abc123"}
         ↓ async
         Worker pulls job → runs AI pipeline
         ↓
Client → GET /jobs/abc123 → {status: "complete", result: {...}}
```

Tools: Celery + Redis, BullMQ + Redis, AWS SQS + Lambda, Cloud Tasks.

---

## Cost Management

### Token cost optimization
- Cache aggressively (semantic + exact)
- Use smaller models for routing/classification
- Compress context: summarize history, filter irrelevant chunks
- Batch non-urgent requests (Anthropic/OpenAI batch APIs: ~50% cheaper)

### Cost monitoring
```python
# Track tokens per request
@app.middleware("http")
async def track_tokens(request, call_next):
    response = await call_next(request)
    # Log token usage from LLM response headers/body
    metrics.increment("llm.tokens.input", value=input_tokens)
    metrics.increment("llm.tokens.output", value=output_tokens)
    return response
```

Alert when cost/request rises >20% week-over-week.

---

## Fallback & Resilience

```python
async def call_llm_with_fallback(prompt: str) -> str:
    providers = [
        ("anthropic", call_anthropic),
        ("openai", call_openai),
        ("cached_response", get_closest_cached),
    ]
    
    for name, fn in providers:
        try:
            return await asyncio.wait_for(fn(prompt), timeout=30)
        except (TimeoutError, APIError) as e:
            logger.warning(f"{name} failed: {e}, trying next...")
    
    return "I'm having trouble connecting right now. Please try again."
```

---

## Model Serving (Self-Hosted)

When to self-host: data privacy requirements, very high volume (>1M req/day), need for fine-tuned models.

| Tool | Best For |
|---|---|
| **vLLM** | High-throughput production serving, continuous batching |
| **Ollama** | Local dev, small team self-hosting |
| **TGI (HuggingFace)** | HuggingFace model ecosystem |
| **LiteLLM** | Unified API across 100+ providers |

Minimum hardware for 7B model: 16GB VRAM (1x A10G).
For 70B model: 80GB VRAM (2x A100) or 4x A10G with tensor parallelism.

---

## Observability Stack

### Recommended open-source stack
- **Tracing**: OpenTelemetry → Jaeger or Grafana Tempo
- **Metrics**: Prometheus + Grafana
- **LLM-specific**: Langfuse (self-hosted) or Helicone
- **Logs**: Loki or ELK stack

### Key dashboards to build
1. **Request dashboard**: QPS, error rate, latency P50/P95/P99
2. **Cost dashboard**: tokens/day, cost/request, cost by model
3. **Quality dashboard**: user ratings, hallucination flags, fallback rate
4. **Infrastructure**: GPU utilization (if self-hosted), cache hit rate
