---
title: "RAG Explained: How AI Reads YOUR Data (With Code)"
description: "A clear breakdown of Retrieval-Augmented Generation — vector embeddings, chunking strategies, retrieval pipelines, and a working code example you can run today."
tags: ["ai", "machinelearning", "python", "tutorial"]
canonical_url: https://techai-explained.github.io/techai-explained/articles/rag-explained/
published: false
---

You ask an LLM about your company's internal docs and it makes things up. You ask it about last quarter's revenue and it hallucinates a number. **RAG — Retrieval-Augmented Generation — is how you fix this.** It lets AI answer questions using your own data, accurately.

Here's exactly how it works and how to build one.

## What Is RAG? (One Sentence)

> RAG is a pattern where you **RETRIEVE** relevant documents from your data, then **AUGMENT** the LLM's prompt with those documents, so it can **GENERATE** an answer grounded in real information.

```
1. RETRIEVE                2. AUGMENT               3. GENERATE
─────────                  ───────                   ────────
User asks:                 System prompt +           LLM generates
"What's our               retrieved docs +           answer using
 refund policy?"          user question               the context

      │                         │                         │
      ▼                         ▼                         ▼
┌──────────┐            ┌──────────────┐         ┌──────────────┐
│ Search   │            │ "Context:    │         │ "Our refund  │
│ vector   │────────►   │  [doc1]      │────►    │  policy      │
│ database │            │  [doc2]      │         │  allows      │
│ for top  │            │              │         │  returns     │
│ matches  │            │ Question:    │         │  within 30   │
└──────────┘            │  What's our  │         │  days..."    │
                        │  refund...?" │         └──────────────┘
                        └──────────────┘
```

## Why RAG Instead of Fine-Tuning?

Fine-tuning bakes knowledge INTO the model. RAG FETCHES knowledge at query time. Here's why that matters:

| | Fine-Tuning | RAG |
|---|---|---|
| Update data | Retrain model (hours/days) | Update database (seconds) |
| Cost | High (GPU training) | Low (embedding + search) |
| Citations | Cannot cite sources | Can cite exact documents |
| Accuracy | Can hallucinate trained data | Grounded in retrieved docs |

For most production use cases, RAG wins on cost, speed, and explainability.

## Vector Embeddings: The Magic Behind RAG

An embedding model converts text into a list of numbers — a vector — that captures the **meaning** of the text. Similar meanings produce similar vectors. "How to return a product" and "refund policy for items" have very different words but very similar vectors.

```
Vector space (simplified to 2D):

    ▲
    │    • "refund policy"
    │    • "return items"         • "shipping rates"
    │    • "money back"           • "delivery times"
    │  ★ QUERY                    • "tracking order"
    │  "how to get a refund"
    │
    │         • "product specs"
    │         • "item dimensions"
    └──────────────────────────────────────►

★ = query vector (closest to refund cluster)
```

When a user asks a question, you embed that question and find the closest document vectors. Those are your retrieved chunks.

```python
# Embedding a document
response = openai.embeddings.create(
    input="Our refund policy allows returns within 30 days",
    model="text-embedding-3-small"
)
vector = response.data[0].embedding  # [0.023, -0.041, 0.078, ...]
# 1536 dimensions of meaning
```

## The Full RAG Pipeline

```
INDEXING (one-time)                    QUERYING (per question)
───────────────────                    ─────────────────────

Documents ──► Chunking ──► Embedding   User question
                              │            │
                              ▼            ▼
                        ┌──────────┐  Embed question
                        │ Vector   │       │
                        │ Database │◄──────┘
                        └────┬─────┘  Similarity search
                             │
                             ▼
                        Top K chunks
                             │
                             ▼
                     ┌──────────────┐
                     │ LLM Prompt:  │
                     │ Context +    │
                     │ Question     │──► Answer with citations
                     └──────────────┘
```

**Indexing phase (run once):**
1. Chunk your documents into smaller pieces
2. Embed each chunk into a vector
3. Store vectors in a vector database (Pinecone, Weaviate, pgvector)

**Query phase (run per question):**
4. Embed the user's question
5. Search the vector database for the most similar chunks (top 3–5)
6. Build the prompt with retrieved chunks as context
7. Send to the LLM and get a grounded answer

### Working Code Example

```python
# Complete RAG pipeline in 20 lines
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Index documents (one-time)
documents = SimpleDirectoryReader("./company-docs").load_data()
index = VectorStoreIndex.from_documents(documents)

# Query (per question)
query_engine = index.as_query_engine(similarity_top_k=3)
response = query_engine.query("What is our refund policy?")

print(response.response)     # The answer
print(response.source_nodes) # The source documents
```

## Chunking: Where Most RAG Systems Fail

Chunking is the most underrated part of RAG. Get it wrong and your system retrieves the wrong context. Get it right and accuracy jumps dramatically.

```
FIXED SIZE CHUNKING           SEMANTIC CHUNKING
───────────────────           ─────────────────
Split every 500 tokens        Split at paragraph/section boundaries

"...end of section A.        "Section A: Refund Policy
Section B: Shipping..."      Our refund policy allows..."
     ↑ splits mid-topic           ↑ splits at natural boundary

Problem: loses context        Better: preserves meaning

RECURSIVE CHUNKING            PARENT-CHILD CHUNKING
───────────────────           ─────────────────────
Split by paragraph,           Embed small chunks (child)
then by sentence,             but retrieve the parent
then by token                 (larger context)

Adapts to document            Best accuracy
structure                     (search precision + full context)
```

**Three rules for chunking:**

1. Keep chunk sizes between **256 and 1024 tokens**. Too small = lose context. Too large = dilute relevance.
2. Add **10–20% overlap** so information at chunk boundaries isn't lost.
3. **Preserve document structure** — headers, sections, and paragraphs are natural boundaries.

## Production Considerations

### Hybrid Search

Vector search alone misses exact matches. If someone searches for "error code E-4521", vector similarity might not find it. **Hybrid search** combines vector search with keyword search — the best of both worlds.

### Re-ranking

Retrieve 20 chunks with vector search, then re-rank the top 20 with a cross-encoder model to find the true top 5. This two-stage approach dramatically improves accuracy.

```
Stage 1: Vector search → 20 candidates (fast, approximate)
Stage 2: Cross-encoder rerank → 5 best matches (slow, precise)
```

### Evaluation

Create a test set of 50–100 questions with known correct answers. Measure:
- **Retrieval accuracy**: did we find the right chunks?
- **Generation accuracy**: did the LLM produce the right answer?

Without evaluation, you're guessing. With eval, you can iterate on every parameter — chunk size, overlap, top-k — and measure the impact.

## Summary

RAG is the pattern that makes AI actually useful with your own data:

- **Retrieve** relevant chunks via vector similarity
- **Augment** the prompt with those chunks as context
- **Generate** a grounded, citable answer

The hard parts are chunking and evaluation. Get those right and you have a system that answers questions accurately with citations — no fine-tuning required.

---

*Published by the **TechAI Explained** team. Follow us for more AI engineering deep dives.*
