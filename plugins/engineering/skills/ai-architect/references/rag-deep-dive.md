# RAG Deep Dive — Advanced Retrieval-Augmented Generation

## Why RAG Fails (and How to Fix It)

### Problem: Retrieval returns irrelevant chunks
**Fix**: Query rewriting — use an LLM to expand/rewrite the query before retrieval.
```python
rewritten = llm.complete(f"Rewrite this query for semantic search: {user_query}")
```

**Fix**: Hypothetical Document Embeddings (HyDE) — generate a fake answer, embed it, search.
```python
fake_doc = llm.complete(f"Write a document that answers: {user_query}")
chunks = vector_db.search(embed(fake_doc))
```

### Problem: Retrieved chunks lack context
**Fix**: Sentence-window retrieval — index sentences but return their surrounding paragraph.
**Fix**: Document metadata — always store title, section header, date alongside chunks.

### Problem: LLM ignores retrieved context
**Fix**: Position context before the question (primacy effect).
**Fix**: Explicitly instruct: "Base your answer ONLY on the context below. If not in context, say so."

### Problem: Chunks are too large / too small
- Too large: retrieval score gets diluted by irrelevant content
- Too small: not enough context for coherent answers
**Fix**: Hierarchical chunking — small chunks for retrieval, parent chunks for context.
- Parent chunk: ~512 tokens, Child chunk: ~128 tokens
- Retrieve child, return parent

---

## Chunking Strategies

| Strategy | Use When |
|---|---|
| Fixed-size (512 tokens) | General purpose, baseline |
| Sentence-based | High precision needed |
| Recursive character splitting | Unstructured text |
| Semantic chunking | Preserving topic coherence |
| Document-structure-aware | PDFs, HTML with clear structure |
| Agentic chunking | LLM decides chunk boundaries |

---

## Hybrid Search

Combine dense (semantic) and sparse (keyword) retrieval for best results:

```python
# Dense score (cosine similarity from embedding)
dense_scores = vector_db.search(query_embedding, top_k=20)

# Sparse score (BM25 keyword match)
sparse_scores = bm25_index.search(query_text, top_k=20)

# Reciprocal Rank Fusion
final_scores = rrf(dense_scores, sparse_scores)
top_chunks = final_scores[:5]
```

RRF formula: `score(d) = Σ 1 / (k + rank(d))` where k=60

---

## Re-Ranking

After retrieval, use a cross-encoder to re-score candidate chunks:
```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
scores = reranker.predict([(query, chunk) for chunk in candidates])
top_chunks = [chunk for _, chunk in sorted(zip(scores, candidates), reverse=True)][:3]
```

Cross-encoders are slower but much more accurate than bi-encoders for re-ranking.

---

## Multi-Vector Retrieval

Store multiple embeddings per document:
- Embed the summary → good for high-level queries
- Embed each section → good for detail queries
- Embed generated questions → good for conversational RAG

---

## Evaluation Metrics for RAG

| Metric | What It Measures | Tool |
|---|---|---|
| Context Precision | Are retrieved chunks relevant? | RAGAs |
| Context Recall | Are all needed chunks retrieved? | RAGAs |
| Answer Faithfulness | Is answer grounded in context? | RAGAs / LLM judge |
| Answer Relevancy | Does answer address the question? | RAGAs |
| Latency P95 | End-to-end response time | Custom |
