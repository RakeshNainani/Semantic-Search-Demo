# Semantic Search Demo

A hands-on AI Engineering project demonstrating how enterprise documents can be converted into embeddings, stored in a vector database, and retrieved using semantic similarity and metadata-aware filtering.

The project intentionally builds the retrieval pipeline from first principles before introducing higher-level RAG frameworks such as LangChain or LangGraph.

The goal is to understand what actually happens inside a modern enterprise semantic-search or Retrieval-Augmented Generation (RAG) system.

---

# 1. Project Overview

Traditional keyword search looks for matching words.

Semantic search instead converts both documents and user queries into numerical vectors called **embeddings** and retrieves content based on semantic similarity.

For example, the query:

```text
What requirements apply to production cloud applications?
```

can retrieve content such as:

```text
This standard defines the minimum architectural requirements
for applications deployed to public cloud environments.
```

even though the wording is not identical.

This project implements that complete retrieval pipeline.

---

# 2. What This Project Demonstrates

The project currently demonstrates:

- Loading enterprise documents from multiple file formats
- Normalizing documents into a common internal model
- Enterprise metadata enrichment
- Paragraph-aware document chunking
- Local embedding generation using SentenceTransformers
- Dense vector representations
- Cosine similarity
- Vector-store abstraction
- In-memory vector search
- Persistent Qdrant vector storage
- Qdrant payload metadata
- Semantic similarity search
- Top-K retrieval
- Similarity-score thresholds
- Metadata filtering
- Multiple metadata filters
- Dynamic command-line search
- Separation of ingestion and query-time retrieval
- Deterministic vector IDs
- Persistent local vector collections

This forms the retrieval foundation required for a future RAG implementation.

---

# 3. Current Architecture

The system has two independent flows.

## 3.1 Document Ingestion

```text
Enterprise Documents
        |
        v
PDF / DOCX / Markdown Loaders
        |
        v
Normalized Document
        |
        v
Metadata Enrichment
        |
        v
Document Chunking
        |
        v
Chunk[]
        |
        v
Embedding Model
        |
        v
Dense Vectors
        |
        v
QdrantVectorStore
        |
        v
Persistent Qdrant Collection
```

---

## 3.2 Query-Time Retrieval

```text
User Query
     |
     v
Embedding Model
     |
     v
Query Embedding
     |
     v
Qdrant
     |
     +----------------------+
     |                      |
     v                      v
Vector Similarity      Metadata Filters
     |                      |
     +-----------+----------+
                 |
                 v
              Top-K
                 |
                 v
          SearchResult[]
```

Document ingestion and query-time retrieval are deliberately separated.

Documents therefore do not need to be reloaded, re-chunked, and re-embedded every time a user performs a search.

---

# 4. Technology Stack

## Language

Python

## Package and Environment Management

`uv`

## Embedding Framework

SentenceTransformers

## Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

The current model produces:

```text
384-dimensional embeddings
```

## Vector Database

Qdrant

The project currently uses **Qdrant Local Mode**, which means:

- Docker is not required
- No external Qdrant server is required
- Vector data is persisted locally
- The same Qdrant concepts are used as with a server deployment

Persistent Qdrant data is stored under:

```text
data/qdrant/
```

## Document Parsing

PDF:

```text
pypdf
```

DOCX:

```text
python-docx
```

Markdown:

Python filesystem APIs

## Numerical Operations

```text
numpy
```

---

# 5. Project Structure

A typical project structure is:

```text
semantic-search-demo/
|
├── data/
│   |
│   ├── docs/
│   │   ├── information_security_policy.pdf
│   │   ├── incident_management_sop.pdf
│   │   ├── cloud_architecture_standard.docx
│   │   ├── vendor_onboarding_process.docx
│   │   ├── travel_and_expense_policy.md
│   │   └── data_access_standard.md
│   |
│   ├── document_metadata.json
│   |
│   └── qdrant/
│
├── src/
│   └── semantic_search_demo/
│       |
│       ├── __init__.py
│       ├── models.py
│       ├── chunker.py
│       ├── embeddings.py
│       ├── similarity.py
│       ├── vector_store.py
│       ├── in_memory_vector_store.py
│       ├── qdrant_vector_store.py
│       ├── ingestion_service.py
│       ├── semantic_search_service.py
│       ├── metadata_loader.py
│       ├── ingest.py
│       ├── query.py
│       |
│       └── loaders/
│           ├── __init__.py
│           ├── document_loader.py
│           ├── pdf_loader.py
│           ├── docx_loader.py
│           └── markdown_loader.py
│
├── inspect_qdrant.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

`inspect_qdrant.py` is currently a diagnostic utility and may later be moved under a dedicated `scripts/` directory.

---

# 6. Core Domain Models

The application normalizes different source formats into shared domain objects.

## Document

A document represents an entire source file.

Conceptually:

```text
Document
|
├── document_id
├── source
├── file_type
├── text
└── metadata
```

Example metadata:

```json
{
  "organization": "Northstar Technologies Pvt. Ltd.",
  "document_owner": "Enterprise Architecture",
  "classification": "Internal",
  "version": "2.4"
}
```

---

## Chunk

Documents are split into smaller semantic retrieval units.

```text
Chunk
|
├── chunk_id
├── document_id
├── source
├── file_type
├── chunk_index
├── text
└── metadata
```

Document metadata is propagated into **every chunk**.

This is important because vector databases retrieve individual chunks rather than entire documents.

---

## SearchResult

Search results currently contain:

```text
SearchResult
|
├── chunk_id
├── document_id
├── source
├── score
└── text
```

---

# 7. Document Corpus

The project uses a fictional enterprise called:

```text
Northstar Technologies Pvt. Ltd.
```

The sample corpus contains several enterprise-style documents.

Examples include:

- Information Security Policy
- Cloud Architecture Standard
- Travel and Expense Policy
- IT Incident Management SOP
- Third-Party Vendor Onboarding Process
- Enterprise Data Access Standard

These documents are intentionally more realistic than basic toy examples because the project is intended to demonstrate enterprise retrieval patterns.

---

# 8. Metadata Registry

Enterprise metadata is stored separately from document text in:

```text
data/document_metadata.json
```

Example:

```json
{
  "cloud_architecture_standard": {
    "organization": "Northstar Technologies Pvt. Ltd.",
    "document_owner": "Enterprise Architecture",
    "classification": "Internal",
    "version": "2.4"
  },

  "information_security_policy": {
    "organization": "Northstar Technologies Pvt. Ltd.",
    "document_owner": "Information Security",
    "classification": "Internal",
    "version": "3.1"
  },

  "travel_and_expense_policy": {
    "organization": "Northstar Technologies Pvt. Ltd.",
    "document_owner": "Finance",
    "classification": "Internal",
    "version": "4.1"
  },

  "incident_management_sop": {
    "organization": "Northstar Technologies Pvt. Ltd.",
    "document_owner": "IT Operations",
    "classification": "Internal",
    "version": "2.2"
  },

  "vendor_onboarding_process": {
    "organization": "Northstar Technologies Pvt. Ltd.",
    "document_owner": "Procurement",
    "classification": "Internal",
    "version": "1.8"
  },

  "data_access_standard": {
    "organization": "Northstar Technologies Pvt. Ltd.",
    "document_owner": "Data Governance",
    "classification": "Internal",
    "version": "2.0"
  }
}
```

This design reflects how enterprise metadata often originates from systems such as:

- SharePoint
- Document Management Systems
- Data Catalogues
- Databases
- Upload APIs
- Content Management Systems
- Security classification systems

rather than necessarily being embedded inside the document body.

---

# 9. Chunking Strategy

The current implementation uses:

```text
Paragraph-aware greedy chunking
```

with a default soft limit of:

```text
800 characters
```

The algorithm:

1. Splits the document on paragraph boundaries.
2. Adds paragraphs to the current chunk.
3. Continues until adding another paragraph would exceed the configured limit.
4. Saves the current chunk.
5. Starts a new chunk.
6. Preserves document metadata on every chunk.

The current implementation intentionally has **no overlap**.

Example:

```text
Document

Paragraph 1
Paragraph 2
Paragraph 3
Paragraph 4
Paragraph 5

        ↓

Chunk 0
Paragraph 1
Paragraph 2

Chunk 1
Paragraph 3
Paragraph 4

Chunk 2
Paragraph 5
```

Future improvements may include:

- token-aware chunking
- recursive chunking
- sentence-aware splitting
- heading-aware chunking
- configurable overlap
- semantic chunking
- parent-child retrieval
- table-aware chunking
- code-aware chunking

---

# 10. Embeddings

The application currently uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

through `SentenceTransformer`.

Example conceptual flow:

```text
Text
 |
 v
Embedding Model
 |
 v
[0.021, -0.044, 0.013, ...]
```

The output vector contains:

```text
384 dimensions
```

Both documents and queries must use the **same embedding model**.

This is an important vector-search data contract.

A collection is effectively tied to:

```text
Embedding Model
+
Vector Dimension
+
Similarity Metric
```

Changing the embedding model may therefore require re-embedding and rebuilding the vector index.

---

# 11. Similarity

The project initially implements cosine similarity manually with NumPy to demonstrate the underlying mathematics.

Conceptually:

```text
cosine_similarity(query_vector, document_vector)
```

measures the angle between vectors.

Higher similarity generally means greater semantic relatedness.

The project later delegates vector ranking to Qdrant.

This progression is intentional:

```text
Manual NumPy similarity
        ↓
Understand fundamentals
        ↓
Vector-store abstraction
        ↓
Qdrant
```

---

# 12. Vector Store Abstraction

The project defines a common:

```text
VectorStore
```

interface.

Current implementations:

```text
VectorStore
    |
    +-- InMemoryVectorStore
    |
    +-- QdrantVectorStore
```

The abstraction allows the application layer to work against a common contract rather than directly depending on one database implementation.

Conceptually:

```text
SemanticSearchService
        |
        v
    VectorStore
        |
   +----+----+
   |         |
Memory     Qdrant
```

This is useful for testing, learning, and future infrastructure replacement.

---

# 13. Qdrant Storage Model

Each chunk becomes a Qdrant point.

Conceptually:

```text
Qdrant Point
|
├── ID
|
├── Vector
│   └── 384-dimensional embedding
|
└── Payload
    ├── chunk_id
    ├── document_id
    ├── source
    ├── file_type
    ├── chunk_index
    ├── text
    ├── organization
    ├── document_owner
    ├── classification
    └── version
```

The vector is used for semantic retrieval.

The payload contains the business context associated with that vector.

---

# 14. Deterministic Vector IDs

Chunk IDs are converted to deterministic UUIDs.

Conceptually:

```text
cloud_architecture_standard-0
        ↓
UUID5
        ↓
Stable Qdrant Point ID
```

This ensures the same chunk receives the same Qdrant point ID during repeated ingestion.

Therefore:

```text
same chunk
   ↓
same UUID
   ↓
Qdrant upsert
   ↓
existing point updated
```

rather than inserting duplicate records every time ingestion runs.

---

# 15. Prerequisites

Before running the project, install:

- Git
- Python
- `uv`

Docker is **not required** for the current implementation because Qdrant is running in local mode.

Use the Python version defined or supported by the project's `pyproject.toml`.

---

# 16. Installing uv

If `uv` is not already installed, install it using the official uv installation instructions appropriate for your operating system.

After installation verify:

```powershell
uv --version
```

You should see the installed uv version.

---

# 17. Clone the Repository

Example:

```powershell
cd C:\Work\code_practise
```

Then:

```powershell
git clone <repository-url>
```

Move into the repository:

```powershell
cd semantic-search-demo
```

---

# 18. Install Project Dependencies

Because the project uses `uv`, install/synchronize dependencies with:

```powershell
uv sync
```

This creates or updates the local virtual environment based on:

```text
pyproject.toml
uv.lock
```

The project uses dependencies including:

```text
sentence-transformers
numpy
qdrant-client
pypdf
python-docx
```

---

# 19. Activate the Virtual Environment

Activation is optional when commands are run through:

```powershell
uv run
```

However, on Windows PowerShell the environment can generally be activated with:

```powershell
.venv\Scripts\Activate.ps1
```

When active, the terminal may show:

```text
(semantic-search-demo)
```

---

# 20. Verify the Document Corpus

Ensure the source documents exist under:

```text
data/docs/
```

Example:

```text
data/docs/
├── information_security_policy.pdf
├── incident_management_sop.pdf
├── cloud_architecture_standard.docx
├── vendor_onboarding_process.docx
├── travel_and_expense_policy.md
└── data_access_standard.md
```

---

# 21. Verify Metadata

Ensure:

```text
data/document_metadata.json
```

contains an entry whose key exactly matches each generated `document_id`.

For example:

```text
cloud_architecture_standard.docx
```

produces:

```text
document_id = cloud_architecture_standard
```

Therefore the metadata registry must use:

```json
"cloud_architecture_standard": {
  ...
}
```

A mismatched identifier will result in missing metadata.

---

# 22. Run Document Ingestion

Ingestion is deliberately separated from querying.

Run:

```powershell
uv run python -m semantic_search_demo.ingest
```

The ingestion pipeline executes:

```text
Documents
   ↓
Load
   ↓
Metadata enrichment
   ↓
Chunk
   ↓
Generate embeddings
   ↓
Qdrant upsert
```

Example output:

```text
Starting document ingestion...
Ingestion completed. 19 chunks indexed.
```

The exact chunk count may change as documents or chunking configuration change.

---

# 23. Qdrant Persistence

Qdrant local data is stored under:

```text
data/qdrant/
```

After ingestion, vectors remain available after the Python process exits.

This means the query process does not need to:

```text
reload source documents
re-chunk documents
recompute document embeddings
```

for every search.

---

# 24. Basic Semantic Search

Run:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?"
```

Example output may resemble:

```text
Query: What requirements apply to production cloud applications?

================================================================================
Rank: 1
Score: 0.6582
Document: cloud_architecture_standard
Chunk: cloud_architecture_standard-0
Source: data\docs\cloud_architecture_standard.docx

Cloud Architecture Standard
...
```

The actual numerical score may vary depending on model/library versions and corpus changes.

---

# 25. Semantic Search vs Keyword Search

A major objective of this project is demonstrating that the query does not need to contain the exact wording from the source document.

Example query:

```text
What requirements apply to production cloud applications?
```

Relevant source text:

```text
This standard defines the minimum architectural requirements
for applications deployed to public cloud environments.
```

Semantic similarity allows these texts to match based on meaning.

---

# 26. Metadata Filtering

The CLI supports restricting semantic search to metadata-defined subsets.

Example:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?" --owner "Enterprise Architecture"
```

The retrieval pipeline becomes:

```text
Query
  ↓
Query Embedding
  ↓
Qdrant
  ↓
Filter:
document_owner = Enterprise Architecture
  ↓
Vector Similarity
  ↓
Top-K Results
```

Only chunks belonging to matching documents are eligible.

---

# 27. Classification Filter

Example:

```powershell
uv run python -m semantic_search_demo.query "How should secrets be managed?" --classification "Internal"
```

This applies:

```text
classification = Internal
```

before returning semantic matches.

---

# 28. File-Type Filtering

Example:

```powershell
uv run python -m semantic_search_demo.query "production security requirements" --file-type "docx"
```

This searches only chunks originating from DOCX documents.

---

# 29. Combining Metadata Filters

Filters can be combined.

Example:

```powershell
uv run python -m semantic_search_demo.query "production cloud security requirements" --owner "Enterprise Architecture" --classification "Internal"
```

Conceptually Qdrant applies:

```text
document_owner = Enterprise Architecture
AND
classification = Internal
```

followed by semantic vector ranking.

---

# 30. Top-K Retrieval

`top_k` controls the maximum number of results returned.

Example:

```powershell
uv run python -m semantic_search_demo.query "production cloud applications" --top-k 2
```

Maximum returned results:

```text
2
```

Another example:

```powershell
uv run python -m semantic_search_demo.query "production cloud applications" --top-k 5
```

Maximum returned results:

```text
5
```

Top-K should not be confused with a relevance threshold.

---

# 31. Similarity Score Threshold

The CLI also supports a minimum similarity score.

Example:

```powershell
uv run python -m semantic_search_demo.query "production cloud applications" --min-score 0.5
```

Conceptually:

```text
Retrieve only results where:

similarity score >= 0.5
```

A lower threshold may return more candidates.

A higher threshold may increase precision but reduce recall.

Similarity scores should **not** be interpreted as calibrated probabilities or confidence values.

For example:

```text
0.65
```

does not mean:

```text
65% confidence
```

Thresholds should eventually be selected through retrieval evaluation rather than intuition.

---

# 32. CLI Options

Current query options include:

```text
query
--owner
--classification
--file-type
--top-k
--min-score
```

Example:

```powershell
uv run python -m semantic_search_demo.query `
"production cloud requirements" `
--owner "Enterprise Architecture" `
--classification "Internal" `
--file-type "docx" `
--top-k 3 `
--min-score 0.3
```

---

# 33. Inspecting Qdrant

A temporary diagnostic script is available:

```text
inspect_qdrant.py
```

Run:

```powershell
uv run python inspect_qdrant.py
```

This can display stored Qdrant payload information such as:

```text
chunk_id
document_id
document_owner
classification
```

Example:

```text
chunk_id: cloud_architecture_standard-0
document_id: cloud_architecture_standard
document_owner: Enterprise Architecture
classification: Internal
```

This is useful when diagnosing metadata-filter failures.

---

# 34. Resetting the Local Vector Database

To completely rebuild the local Qdrant database on Windows PowerShell:

```powershell
Remove-Item .\data\qdrant -Recurse -Force
```

Then rerun ingestion:

```powershell
uv run python -m semantic_search_demo.ingest
```

This is useful during development when:

- payload structures change
- embedding models change
- collection configuration changes
- chunking logic changes
- stale vectors need to be removed

---

# 35. Hugging Face Authentication Warning

When loading the SentenceTransformers model, you may see:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
Please set a HF_TOKEN to enable higher rate limits and faster downloads.
```

This is normally a warning rather than an application failure.

The model can generally still be downloaded and used anonymously.

Configuring a Hugging Face token can improve download limits and authentication behavior but is not mandatory for the basic local project workflow.

---

# 36. Why Ingestion and Querying Are Separate

A key architectural decision is separating:

```text
INGESTION
```

from:

```text
QUERY-TIME RETRIEVAL
```

Ingestion is generally:

- asynchronous
- batch-oriented
- event-driven
- compute-heavy
- less latency-sensitive

Query retrieval is generally:

- synchronous
- user-facing
- latency-sensitive
- high-frequency

Production systems therefore typically scale these workflows independently.

Current architecture:

```text
                   INGESTION

Documents
   ↓
Load
   ↓
Metadata
   ↓
Chunk
   ↓
Embed
   ↓
Qdrant


                    QUERY

User Query
   ↓
Embed Query
   ↓
Qdrant Search
   ↓
Metadata Filter
   ↓
Top-K
   ↓
Search Results
```

---

# 37. Enterprise Retrieval Principles Demonstrated

## Semantic Relevance Is Not Authorization

A semantically relevant document should not automatically be returned.

Enterprise retrieval may eventually require filters based on:

```text
tenant
department
country
business unit
document classification
user groups
roles
entitlements
ACLs
```

For example:

```text
User Query
     ↓
Identity Claims
     ↓
Allowed Metadata Scope
     ↓
Semantic Search
     ↓
Authorized Results
```

The current metadata-filter implementation forms the foundation for that architecture.

---

# 38. Why Metadata Matters

Vector similarity alone answers:

> Which chunks are semantically closest to this query?

Metadata-aware retrieval answers:

> Among the chunks this request is allowed or intended to search, which are semantically closest?

This distinction is essential in enterprise systems.

---

# 39. Current Limitations

The project is intentionally incremental and currently has several limitations.

## Chunking

Current chunking:

- uses character counts rather than tokens
- does not use overlap
- is not heading-aware
- is not semantic
- does not preserve parent-child relationships

## Embeddings

Currently:

- one local embedding model
- no embedding-provider abstraction
- no model version stored in payload
- no embedding cache

## Vector Storage

Currently:

- Qdrant Local Mode
- no hosted Qdrant
- no distributed deployment
- no production backup strategy

## Metadata

Currently:

- metadata is maintained in a static JSON registry
- no metadata schema validation
- no dynamic ACL engine
- no tenant isolation

## Retrieval

Currently:

- dense retrieval only
- no keyword/BM25 search
- no hybrid retrieval
- no reranker
- no query rewriting
- no multi-query retrieval

## Evaluation

Currently:

- no labelled evaluation dataset
- no Recall@K measurement
- no Precision@K measurement
- no MRR
- no retrieval regression suite

## RAG

The project currently stops at retrieval.

It does **not yet** send retrieved context to an LLM for answer generation.

---

# 40. Planned Evolution

The project is intended to evolve approximately through the following stages.

## Stage 1 — Document Ingestion

Completed.

```text
PDF / DOCX / Markdown
        ↓
Normalized Documents
```

## Stage 2 — Chunking

Completed initial implementation.

```text
Documents
   ↓
Paragraph-aware chunks
```

## Stage 3 — Embeddings

Completed.

```text
Chunk Text
   ↓
SentenceTransformer
   ↓
384-dimensional vectors
```

## Stage 4 — Manual Similarity Search

Completed.

```text
Query Embedding
   ↓
Cosine Similarity
   ↓
Ranked Chunks
```

## Stage 5 — Vector Store Abstraction

Completed.

```text
VectorStore
   ├── InMemoryVectorStore
   └── QdrantVectorStore
```

## Stage 6 — Persistent Vector Database

Completed.

```text
Qdrant Local
```

## Stage 7 — Separate Ingestion and Retrieval

Completed.

```text
ingest.py
query.py
```

## Stage 8 — Metadata-Aware Retrieval

Completed initial implementation.

```text
Semantic Search
+
Metadata Filters
```

## Stage 9 — FastAPI

Planned.

Potential endpoints:

```text
GET  /health
POST /ingest
POST /search
```

## Stage 10 — Retrieval Evaluation

Planned.

Potential metrics:

```text
Recall@K
Precision@K
MRR
Hit Rate
```

## Stage 11 — Better Chunking

Planned.

Potential improvements:

```text
token-aware chunking
recursive chunking
overlap
heading propagation
parent-child chunks
```

## Stage 12 — Hybrid Search

Planned.

```text
Dense Semantic Search
        +
Keyword / BM25 Search
        ↓
Combined Ranking
```

## Stage 13 — Reranking

Planned.

```text
Initial Top-K
     ↓
Reranker
     ↓
Better-ranked context
```

## Stage 14 — RAG

Planned.

```text
User Question
      ↓
Retriever
      ↓
Relevant Chunks
      ↓
Prompt / Context Construction
      ↓
LLM
      ↓
Grounded Answer
```

## Stage 15 — Corrective / Advanced RAG

Potential future capabilities:

- query rewriting
- retrieval grading
- corrective retrieval
- web fallback
- multi-query retrieval
- agentic retrieval
- citation generation
- context compression
- guardrails
- observability
- evaluation pipelines

---

# 41. Retrieval Evaluation — Future Direction

A retrieval system should not be evaluated only by looking at similarity scores.

A future evaluation dataset may look like:

```text
Question:
How are secrets stored?

Expected relevant chunks:
cloud_architecture_standard-1
information_security_policy-2
```

Then retrieval can be measured using metrics such as:

```text
Recall@K
Precision@K
MRR
Hit Rate
```

This allows decisions such as:

```text
chunk size
top_k
threshold
embedding model
hybrid-search weights
reranker choice
```

to be based on evidence rather than intuition.

---

# 42. Important AI Engineering Lessons

This project intentionally demonstrates several important principles.

### Embeddings are representations, not answers

An embedding converts content into a numerical representation suitable for comparison.

### Similarity score is not confidence

A cosine similarity score is not a calibrated probability.

### Chunking is part of retrieval architecture

The semantic unit chosen during chunking determines what gets:

- embedded
- indexed
- retrieved
- cited
- eventually sent to an LLM

### Embedding configuration is part of the index contract

Changing embedding model or dimension can require rebuilding the vector index.

### Vector databases store more than vectors

Production retrieval typically requires:

```text
vector
+
text
+
metadata
+
security context
```

### Metadata filtering is fundamental to enterprise retrieval

Semantic relevance alone is insufficient when users have different access permissions or business scopes.

### Persistent vector databases separate ingestion from querying

Documents should not normally be re-embedded for every search request.

### Retrieval should be evaluated independently of generation

Before building an LLM answer layer, retrieval quality should first be understood and measured.

---

# 43. Example End-to-End Workflow

Start with a clean database:

```powershell
Remove-Item .\data\qdrant -Recurse -Force
```

Ingest documents:

```powershell
uv run python -m semantic_search_demo.ingest
```

Search the entire corpus:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?"
```

Search only Enterprise Architecture documents:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?" --owner "Enterprise Architecture"
```

Search Procurement documents:

```powershell
uv run python -m semantic_search_demo.query "What is required before giving a vendor production access?" --owner "Procurement"
```

Search only internal documents:

```powershell
uv run python -m semantic_search_demo.query "How should secrets be stored?" --classification "Internal"
```

Limit results:

```powershell
uv run python -m semantic_search_demo.query "cloud security" --top-k 3
```

Apply a similarity threshold:

```powershell
uv run python -m semantic_search_demo.query "cloud security" --min-score 0.4
```

Combine filters:

```powershell
uv run python -m semantic_search_demo.query "production cloud requirements" --owner "Enterprise Architecture" --classification "Internal" --top-k 3
```

---

# 44. Git Recommendations

The local Qdrant database should normally not be committed.

Add:

```text
data/qdrant/
```

to `.gitignore`.

Typical entries include:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
data/qdrant/
```

Source documents may or may not be committed depending on licensing, confidentiality, repository purpose, and project policy.

The sample documents in this project are fictional training data.

---

# 45. Suggested Development Workflow

When changing ingestion logic:

```text
1. Update code
2. Verify document loading
3. Verify metadata
4. Verify chunks
5. Rebuild Qdrant if required
6. Run semantic searches
7. Test filters
8. Commit the checkpoint
```

Useful verification sequence:

```powershell
uv run python -m semantic_search_demo.ingest
```

then:

```powershell
uv run python inspect_qdrant.py
```

then:

```powershell
uv run python -m semantic_search_demo.query "your query"
```

---

# 46. Current Learning Outcome

At the current checkpoint, the project demonstrates the core retrieval layer behind a production-style RAG application:

```text
Enterprise Documents
        ↓
Document Parsing
        ↓
Metadata Enrichment
        ↓
Chunking
        ↓
Embedding Generation
        ↓
Persistent Vector Database
        ↓
Metadata-Constrained Semantic Retrieval
        ↓
Ranked Context
```

The next major milestone is to expose this functionality through a service API and then progressively add retrieval evaluation and RAG generation.

---

# 47. Next Milestone

The next implementation stage is expected to introduce **FastAPI**.

Target architecture:

```text
Client
  |
  v
FastAPI
  |
  +----------------------+
  |                      |
  v                      v
POST /search        POST /ingest
  |                      |
  v                      v
SemanticSearch      IngestionService
  |                      |
  +----------+-----------+
             |
             v
           Qdrant
```

Potential endpoints:

```text
GET /health
POST /search
POST /ingest
```

This will move the project from a command-line learning application toward a reusable AI retrieval service.

---

# 48. Project Purpose

This repository is primarily an **AI Engineering learning project**.

Its objective is not to hide retrieval behavior behind a framework.

Instead, it incrementally exposes the underlying concepts:

```text
Documents
→ Chunking
→ Embeddings
→ Similarity
→ Vector Index
→ Metadata
→ Retrieval
→ Evaluation
→ RAG
```

Understanding these components individually makes it much easier to design, debug, evaluate, and operate enterprise AI and RAG systems later.