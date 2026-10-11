# Semantic Search Demo

A hands-on AI Engineering project that demonstrates how enterprise documents can be ingested, chunked, embedded, indexed in a vector database, exposed through an API, evaluated objectively, and retrieved using semantic similarity plus metadata filtering.

The project is intentionally built incrementally from first principles before introducing full Retrieval-Augmented Generation (RAG).

The objective is to understand the architecture behind enterprise retrieval systems instead of hiding the implementation behind high-level frameworks.

---

# 1. Project Status

Current progress:

```text
✅ Stage 1   Document Ingestion
✅ Stage 2   Initial Chunking
✅ Stage 3   Embeddings
✅ Stage 4   Semantic Similarity Search
✅ Stage 5   Vector Store Abstraction
✅ Stage 6   Persistent Qdrant Vector Database
✅ Stage 7   Separate Ingestion and Query Pipelines
✅ Stage 8   Metadata-Aware Retrieval
✅ Stage 9   FastAPI Service
✅ Stage 10  Retrieval Evaluation Framework
✅ Stage 11  Evaluated Token-Aware Chunking

➡️ Stage 12  Hybrid Search
⏳ Stage 13  Reranking
⏳ Stage 14  Full RAG
⏳ Stage 15  Advanced / Corrective RAG
```

---

# 2. Project Objective

The project demonstrates the retrieval layer that sits underneath a production-style RAG system.

The current architecture supports:

- PDF ingestion
- DOCX ingestion
- Markdown ingestion
- document normalization
- enterprise metadata
- token-aware chunking
- overlapping chunks
- local embedding generation
- semantic similarity
- persistent vector storage
- metadata filtering
- CLI search
- FastAPI endpoints
- ingestion/query separation
- retrieval evaluation
- chunking-strategy comparison

---

# 3. Current Architecture

## 3.1 Ingestion Flow

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
Token-Aware Chunking
        |
        v
Chunk[]
        |
        v
Embedding Model
        |
        v
Dense Embeddings
        |
        v
Qdrant Vector Store
        |
        v
Persistent Vector Index
```

---

## 3.2 Query Flow

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
     +-----------------------+
     |                       |
     v                       v
Vector Similarity      Metadata Filters
     |                       |
     +-----------+-----------+
                 |
                 v
           Score Threshold
                 |
                 v
               Top-K
                 |
                 v
          SearchResult[]
```

---

## 3.3 API Flow

```text
HTTP Client
     |
     v
FastAPI
     |
     +---------------------------+
     |            |              |
     v            v              v
 /health       /search        /ingest
                  |              |
                  v              v
       SemanticSearchService  IngestionService
                  |              |
                  +------+-------+
                         |
                         v
                  EmbeddingService
                         |
                         v
                       Qdrant
```

---

# 4. Technology Stack

## Language

Python

## Package Management

`uv`

## API Framework

FastAPI

## Data Validation

Pydantic

## Embeddings

SentenceTransformers

Current model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Embedding dimension:

```text
384
```

## Vector Database

Qdrant

Current deployment mode:

```text
Qdrant Local Mode
```

No Docker or external Qdrant server is required for the current learning project.

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

Native Python file handling.

## Numerical Operations

```text
numpy
```

---

# 5. Project Structure

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
│   ├── evaluation/
│   │   ├── retrieval_cases.json
│   │   └── chunking_cases.json
│   |
│   ├── document_metadata.json
│   |
│   └── qdrant/
│
├── src/
│   └── semantic_search_demo/
│       |
│       ├── __init__.py
│       |
│       ├── models.py
│       ├── embeddings.py
│       ├── similarity.py
│       |
│       ├── chunking_strategy.py
│       ├── chunker.py
│       ├── token_chunker.py
│       |
│       ├── vector_store.py
│       ├── in_memory_vector_store.py
│       ├── qdrant_vector_store.py
│       |
│       ├── ingestion_service.py
│       ├── semantic_search_service.py
│       |
│       ├── metadata_loader.py
│       |
│       ├── evaluation_models.py
│       ├── evaluation_loader.py
│       ├── evaluation_metrics.py
│       ├── retrieval_evaluator.py
│       ├── evidence_evaluator.py
│       |
│       ├── evaluate.py
│       ├── compare_chunking.py
│       |
│       ├── api_models.py
│       ├── api.py
│       |
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
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

---

# 6. Sample Enterprise Corpus

The sample corpus represents a fictional enterprise:

```text
Northstar Technologies Pvt. Ltd.
```

Documents include:

- Information Security Policy
- Cloud Architecture Standard
- Travel and Expense Policy
- IT Incident Management SOP
- Third-Party Vendor Onboarding Process
- Enterprise Data Access Standard

The documents are intentionally realistic enough to demonstrate enterprise retrieval patterns.

---

# 7. Core Domain Models

## Document

A normalized enterprise document.

```text
Document
|
├── document_id
├── source
├── file_type
├── text
└── metadata
```

Example:

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

Documents are divided into smaller retrieval units.

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

Every chunk inherits its parent document's metadata.

---

## SearchResult

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

# 8. Enterprise Metadata

Metadata is maintained separately in:

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
  }
}
```

This models how metadata is often sourced in enterprises from systems such as:

- SharePoint
- Document Management Systems
- Data Catalogues
- Databases
- Upload APIs
- CMS platforms
- Governance systems
- Security classification systems

Metadata does not need to exist inside the document body.

---

# 9. Initial Chunking Baseline

The original chunking strategy used:

```text
Paragraph-aware greedy chunking
800-character soft limit
No overlap
```

This version is retained as:

```text
ParagraphChunker
```

It serves as the baseline for retrieval experiments.

---

# 10. Current Default Chunking Strategy

The current default is:

```text
TokenAwareChunker
```

Configuration:

```text
Maximum target chunk size: 220 tokens
Overlap:                  30 tokens
```

The splitting hierarchy is:

```text
Document
   |
   v
Paragraph
   |
   +-- fits within token limit
   |       |
   |       v
   |      keep
   |
   +-- too large
           |
           v
        Sentence
           |
           +-- fits
           |    |
           |    v
           |   keep
           |
           +-- too large
                |
                v
           token-level split
```

Chunks are then packed greedily while staying within the configured token target.

---

# 11. Why Token-Aware Chunking

The original strategy measured:

```text
characters
```

The improved strategy measures:

```text
tokens
```

This is more aligned with how embedding models and LLMs process text.

The embedding model tokenizer is reused for chunk sizing.

Advantages include:

- model-aware chunk sizing
- reduced accidental truncation
- consistent embedding inputs
- better boundary handling
- controlled context overlap
- more reliable retrieval experiments

---

# 12. Chunk Overlap

The token-aware strategy currently uses:

```text
30-token overlap
```

Conceptually:

```text
Chunk 1
[A B C D E]

Chunk 2
      [D E F G H]
```

Overlap reduces the chance that important context is lost when information spans a chunk boundary.

Too much overlap, however, can increase:

- duplicate retrieval
- index size
- embedding cost
- context redundancy

Therefore overlap is a retrieval parameter that should be evaluated rather than chosen arbitrarily.

---

# 13. Embedding Model

Current embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Output:

```text
384-dimensional dense vector
```

Conceptually:

```text
Text
  |
  v
Embedding Model
  |
  v
[0.021, -0.044, 0.013, ...]
```

Both document chunks and queries must use a compatible embedding model.

---

# 14. Embedding Data Contract

The vector index is effectively tied to:

```text
Embedding Model
+
Embedding Dimension
+
Distance Metric
```

Changing the embedding model may require rebuilding the vector index.

For example:

```text
MiniLM
384 dimensions
Cosine
```

is not automatically compatible with:

```text
Another Model
1024 dimensions
Dot Product
```

---

# 15. Similarity Search

The project first implements cosine similarity manually using NumPy.

This demonstrates:

```text
Query Embedding
       ↓
Cosine Similarity
       ↓
Rank Scores
       ↓
Top-K
```

The project then delegates nearest-neighbor search to Qdrant.

This progression is intentional:

```text
Understand the mathematics
        ↓
Implement manually
        ↓
Abstract vector storage
        ↓
Use vector database
```

---

# 16. Vector Store Abstraction

The application defines:

```text
VectorStore
```

implementations:

```text
VectorStore
     |
     +-- InMemoryVectorStore
     |
     +-- QdrantVectorStore
```

The service layer depends on the abstraction rather than directly depending on Qdrant.

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

---

# 17. Qdrant Storage

Each chunk is represented in Qdrant as:

```text
Qdrant Point
|
├── ID
├── Vector
└── Payload
```

Example payload:

```text
chunk_id
document_id
source
file_type
chunk_index
text
organization
document_owner
classification
version
chunking_strategy
```

The vector determines semantic similarity.

The payload contains business and retrieval context.

---

# 18. Deterministic Point IDs

Chunk IDs are converted into deterministic UUIDs.

```text
cloud_architecture_standard-0
        |
        v
UUID5
        |
        v
Stable Qdrant Point ID
```

Therefore repeated ingestion uses:

```text
same chunk
   |
same UUID
   |
Qdrant upsert
   |
existing point updated
```

instead of creating duplicates.

---

# 19. Ingestion and Query Separation

Document ingestion and query-time retrieval are separate workflows.

## Ingestion

```text
Documents
   |
   v
Load
   |
   v
Metadata
   |
   v
Chunk
   |
   v
Embed
   |
   v
Qdrant
```

## Query

```text
Query
   |
   v
Embed Query
   |
   v
Qdrant Search
   |
   v
Results
```

The query path therefore does not need to:

```text
reload PDFs
reload DOCX files
re-chunk documents
recompute document embeddings
```

for every request.

---

# 20. Metadata-Aware Retrieval

The system supports payload-based filtering.

Example:

```text
document_owner = Enterprise Architecture
```

Retrieval becomes:

```text
Query
   |
   v
Embedding
   |
   v
Qdrant
   |
   +--------------------+
   |                    |
Similarity          Metadata Filter
   |                    |
   +---------+----------+
             |
             v
           Top-K
```

Metadata filters currently include:

- document owner
- classification
- file type

---

# 21. Why Metadata Filtering Matters

Semantic relevance does not mean authorization.

An enterprise retrieval system may eventually need constraints such as:

```text
tenant_id
department
country
business_unit
classification
role
group
entitlement
ACL
```

Future architecture:

```text
User
 |
 v
Identity / Claims
 |
 v
Allowed Retrieval Scope
 |
 v
Vector Search
 |
 v
Authorized Results
```

---

# 22. Prerequisites

Install:

- Git
- Python
- uv

Docker is not required for the current project.

Verify:

```powershell
python --version
```

```powershell
uv --version
```

```powershell
git --version
```

---

# 23. Clone Repository

Example:

```powershell
cd C:\Work\code_practise
```

```powershell
git clone <repository-url>
```

```powershell
cd semantic-search-demo
```

---

# 24. Install Dependencies

Run:

```powershell
uv sync
```

Dependencies include:

```text
sentence-transformers
numpy
qdrant-client
pypdf
python-docx
fastapi
uvicorn
pydantic
```

---

# 25. Virtual Environment

The project can be run entirely with:

```powershell
uv run
```

Manual environment activation is optional.

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

---

# 26. Prepare Documents

Place source documents in:

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

# 27. Prepare Metadata

Ensure:

```text
data/document_metadata.json
```

contains matching `document_id` keys.

Example:

```text
cloud_architecture_standard.docx
```

becomes:

```text
cloud_architecture_standard
```

Metadata key:

```json
{
  "cloud_architecture_standard": {
    "document_owner": "Enterprise Architecture"
  }
}
```

The names must match exactly.

---

# 28. Run Ingestion

Run:

```powershell
uv run python -m semantic_search_demo.ingest
```

Expected output resembles:

```text
Starting document ingestion...
Ingestion completed. 17 chunks indexed.
```

The chunk count may change when:

- corpus changes
- chunking strategy changes
- token size changes
- overlap changes

---

# 29. Qdrant Persistence

Qdrant data is stored locally under:

```text
data/qdrant/
```

This directory should generally not be committed to Git.

Add to `.gitignore`:

```text
data/qdrant/
```

---

# 30. Basic CLI Search

Example:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?"
```

Example result:

```text
Rank: 1
Score: 0.65
Document: cloud_architecture_standard
Chunk: cloud_architecture_standard-0
```

---

# 31. Owner Filter

Example:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?" --owner "Enterprise Architecture"
```

Only matching owner documents should be eligible.

---

# 32. Classification Filter

Example:

```powershell
uv run python -m semantic_search_demo.query "How should secrets be stored?" --classification "Internal"
```

---

# 33. File-Type Filter

Example:

```powershell
uv run python -m semantic_search_demo.query "cloud security" --file-type "docx"
```

---

# 34. Multiple Filters

Example:

```powershell
uv run python -m semantic_search_demo.query "production cloud requirements" --owner "Enterprise Architecture" --classification "Internal"
```

Filters are combined using AND logic.

Conceptually:

```text
document_owner = Enterprise Architecture
AND
classification = Internal
```

---

# 35. Top-K

Example:

```powershell
uv run python -m semantic_search_demo.query "cloud security" --top-k 3
```

`top_k` means:

```text
Maximum number of retrieved results
```

---

# 36. Score Threshold

Example:

```powershell
uv run python -m semantic_search_demo.query "cloud security" --min-score 0.4
```

Do not interpret similarity as a probability.

```text
score = 0.65
```

does not mean:

```text
65% confidence
```

Thresholds should be evaluated empirically.

---

# 37. Start FastAPI

Run:

```powershell
uv run fastapi dev src/semantic_search_demo/api.py
```

Development server:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 38. API Endpoints

## Health

```text
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Search

```text
POST /search
```

Example request:

```json
{
  "query": "What requirements apply to production cloud applications?",
  "top_k": 5,
  "min_score": 0,
  "filters": {
    "document_owner": "Enterprise Architecture"
  }
}
```

Example response structure:

```json
{
  "query": "What requirements apply to production cloud applications?",
  "result_count": 4,
  "results": [
    {
      "chunk_id": "cloud_architecture_standard-0",
      "document_id": "cloud_architecture_standard",
      "source": "data\\docs\\cloud_architecture_standard.docx",
      "score": 0.65,
      "text": "..."
    }
  ]
}
```

---

## Ingest

```text
POST /ingest
```

Current implementation ingests:

```text
data/docs/
```

Example response:

```json
{
  "status": "completed",
  "chunks_indexed": 17
}
```

For the learning project this endpoint is synchronous.

In production, large ingestion workloads would usually be implemented using:

```text
API
 ↓
Job Queue
 ↓
Worker
 ↓
Embedding
 ↓
Vector DB
```

---

# 39. API Model Loading

The embedding model is initialized during FastAPI startup.

```text
API startup
    |
    v
Load embedding model
    |
    v
Open Qdrant
    |
    v
Create services
    |
    v
API ready
```

The model is not reloaded for every request.

---

# 40. Retrieval Evaluation

The project includes an evaluation framework.

Ground-truth dataset:

```text
data/evaluation/retrieval_cases.json
```

Each case contains:

```text
query
+
expected relevant chunks
```

Example:

```json
{
  "query_id": "vendor-001",
  "query": "What is required before a vendor gets production access?",
  "relevant_chunk_ids": [
    "vendor_onboarding_process-1"
  ]
}
```

---

# 41. Retrieval Metrics

The project currently supports:

```text
Precision@K
Recall@K
Hit Rate@K
MRR
```

---

## Precision@K

Answers:

> Of the retrieved chunks, how many were relevant?

Example:

```text
4 retrieved
2 relevant
```

```text
Precision@4 = 0.50
```

---

## Recall@K

Answers:

> Of all relevant chunks, how many were retrieved?

Example:

```text
3 relevant chunks exist
2 retrieved
```

```text
Recall@K = 0.67
```

---

## Hit Rate@K

Answers:

> Did at least one relevant chunk appear in the Top-K?

```text
Yes → 1
No  → 0
```

---

## Mean Reciprocal Rank

Measures how early the first relevant result appears.

Example:

```text
Rank 1 relevant → RR = 1.0

Rank 2 relevant → RR = 0.5

Rank 3 relevant → RR = 0.333
```

MRR is the average reciprocal rank across evaluation queries.

---

# 42. Run Retrieval Evaluation

Run:

```powershell
uv run python -m semantic_search_demo.evaluate
```

The evaluator compares multiple retrieval depths:

```text
K=1
K=3
K=5
```

Example summary:

```text
OVERALL METRICS @ K=3

Mean Precision@3: ...
Mean Recall@3: ...
Hit Rate@3: ...
MRR: ...
```

---

# 43. Why Multiple K Values

Lower K generally means:

```text
less context
less noise
potentially lower recall
```

Higher K generally means:

```text
more context
higher recall
potentially more noise
```

Therefore retrieval depth should be measured rather than assumed.

---

# 44. Chunking Experiment

Stage 11 introduced a controlled chunking experiment.

Baseline:

```text
ParagraphChunker
800 characters
0 overlap
```

Candidate:

```text
TokenAwareChunker
220 tokens
30-token overlap
```

All other major variables were held constant:

```text
same corpus
same embedding model
same vector database
same queries
same evaluation criteria
```

Only the chunking strategy changed.

---

# 45. Evidence-Based Chunking Evaluation

Changing chunk boundaries changes chunk IDs.

Therefore the Stage 11 comparison uses stable evidence phrases instead of specific chunk IDs.

Dataset:

```text
data/evaluation/chunking_cases.json
```

Example:

```json
{
  "query_id": "cloud-secrets-001",
  "query": "Where should passwords and application secrets be stored?",
  "evidence_phrases": [
    "Passwords, API keys, certificates, and connection strings must be stored in approved secret-management services",
    "Secrets must not be stored in source-code repositories."
  ]
}
```

This allows fair comparison across different chunking strategies.

---

# 46. Evidence Recall

The chunking evaluator measures:

```text
Evidence Recall@K
```

This answers:

> Of the known supporting evidence statements, how many appeared in the retrieved chunks?

This is more stable than chunk-ID-based ground truth when chunk boundaries differ.

---

# 47. Compare Chunking Strategies

Run:

```powershell
uv run python -m semantic_search_demo.compare_chunking
```

The comparison evaluates:

```text
K=1
K=3
K=5
```

for both strategies.

Example output structure:

```text
SUMMARY — K=3

Metric                 Baseline     Token-aware
Precision                 ...
Evidence Recall           ...
Hit Rate                  ...
MRR                       ...
```

---

# 48. Experimentation Principle

Retrieval changes should follow:

```text
Propose change
     |
     v
Create isolated experiment
     |
     v
Keep unrelated variables fixed
     |
     v
Run evaluation
     |
     v
Compare metrics
     |
     v
Promote only if better
```

This is an important AI Engineering principle.

A strategy should not be adopted merely because it appears more sophisticated.

---

# 49. Current Default

After evaluation, the project uses:

```text
TokenAwareChunker
```

as the default ingestion strategy.

Configuration:

```text
max_tokens     = 220
overlap_tokens = 30
```

The original `ParagraphChunker` remains available as the baseline/reference implementation.

---

# 50. Rebuilding the Vector Index

If you change:

- embedding model
- chunking strategy
- metadata schema
- vector dimensions
- distance metric
- important payload structure

the safest development workflow is often:

```powershell
Remove-Item .\data\qdrant -Recurse -Force
```

then:

```powershell
uv run python -m semantic_search_demo.ingest
```

Do not do this against a production vector database without a proper migration strategy.

---

# 51. Hugging Face Warning

You may see:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This usually does not indicate an application failure.

The embedding model can generally still be downloaded and used anonymously.

A Hugging Face token can optionally be configured for authenticated access and higher download limits.

---

# 52. Current Limitations

The project is intentionally incomplete.

## Search

Currently:

```text
Dense semantic retrieval only
```

Not yet implemented:

```text
BM25
keyword retrieval
hybrid search
```

---

## Ranking

No second-stage reranker yet.

---

## Generation

No LLM answer generation yet.

This project currently stops at retrieval.

---

## Security

Metadata filtering exists, but there is not yet a real:

```text
authentication system
authorization engine
ACL service
tenant model
identity provider
```

---

## Ingestion

Current ingestion is:

```text
local filesystem based
```

Future sources may include:

```text
SharePoint
S3
Azure Blob Storage
databases
APIs
web content
```

---

## Evaluation

Current evaluation corpus is intentionally small.

A production evaluation suite should include:

- significantly more queries
- paraphrased queries
- negative queries
- ambiguous questions
- security-filter cases
- domain-specific terminology
- regression tracking

---

# 53. Stage Roadmap

## Stage 1 — Document Ingestion

Completed.

---

## Stage 2 — Initial Chunking

Completed.

---

## Stage 3 — Embeddings

Completed.

---

## Stage 4 — Semantic Similarity

Completed.

---

## Stage 5 — VectorStore Abstraction

Completed.

---

## Stage 6 — Persistent Qdrant

Completed.

---

## Stage 7 — Separate Ingestion and Query

Completed.

---

## Stage 8 — Metadata Retrieval

Completed.

---

## Stage 9 — FastAPI

Completed.

Endpoints:

```text
GET  /health
POST /search
POST /ingest
```

---

## Stage 10 — Retrieval Evaluation

Completed.

Metrics:

```text
Precision@K
Recall@K
Hit Rate@K
MRR
```

---

## Stage 11 — Better Chunking

Completed.

Current default:

```text
Token-aware hierarchical chunking
220 tokens
30-token overlap
```

---

## Stage 12 — Hybrid Search

Next.

Target:

```text
Dense Vector Retrieval
          +
Lexical Retrieval / BM25
          |
          v
     Fusion Ranking
```

This helps queries containing exact terms such as:

```text
policy IDs
product codes
error codes
acronyms
names
technical identifiers
```

where pure semantic retrieval may underperform.

---

## Stage 13 — Reranking

Planned.

```text
Initial Candidates
       |
       v
Reranker
       |
       v
Better Top Results
```

---

## Stage 14 — RAG

Planned.

```text
Question
   |
   v
Retriever
   |
   v
Relevant Context
   |
   v
Prompt Construction
   |
   v
LLM
   |
   v
Grounded Answer
```

---

## Stage 15 — Advanced / Corrective RAG

Potential capabilities:

- retrieval grading
- query rewriting
- corrective retrieval
- context compression
- multi-query retrieval
- fallback retrieval
- citation generation
- agentic retrieval
- guardrails
- observability
- answer evaluation

---

# 54. Enterprise Retrieval Architecture Direction

The project is evolving toward:

```text
                    User
                     |
                     v
                API Gateway
                     |
                     v
                  FastAPI
                     |
                     v
              Query Processing
                     |
             +-------+-------+
             |               |
             v               v
       Dense Search      Lexical Search
             |               |
             +-------+-------+
                     |
                     v
                Fusion
                     |
                     v
                Reranker
                     |
                     v
            Security Filtering
                     |
                     v
               Top Context
                     |
                     v
                    LLM
                     |
                     v
             Grounded Answer
```

Not all components are implemented yet.

---

# 55. Key Engineering Lessons

## Embeddings are representations

They are not answers.

---

## Similarity is not confidence

A similarity score is not a calibrated probability.

---

## Chunking affects retrieval quality

Chunking determines what is:

```text
embedded
indexed
retrieved
ranked
cited
sent to an LLM
```

---

## Vector indexes have a data contract

The embedding model, vector dimension, and similarity metric must remain compatible.

---

## Metadata is part of retrieval architecture

Enterprise vector search typically involves:

```text
vector
+
content
+
metadata
+
security context
```

---

## Retrieval and generation should be evaluated separately

A poor retriever cannot reliably support a good RAG system.

---

## Retrieval changes require experiments

Do not assume:

```text
more advanced algorithm = better result
```

Measure it.

---

## Ingestion and online retrieval scale differently

Ingestion is generally:

```text
batch
asynchronous
compute-heavy
```

Retrieval is generally:

```text
online
latency-sensitive
high-frequency
```

These workloads should remain architecturally separable.

---

# 56. Recommended Development Workflow

When changing retrieval behavior:

```text
1. Modify one major variable
2. Rebuild isolated index
3. Run evaluation
4. Compare against baseline
5. Inspect failures
6. Decide whether to promote
7. Update default configuration
8. Commit the completed stage
```

---

# 57. Git Checkpoints

The project follows stage-based commits.

Example:

```text
Stage 9
feat: expose semantic search and ingestion with FastAPI

Stage 10
feat: add retrieval evaluation framework and baseline metrics

Stage 11
feat: add evaluated token-aware chunking strategy
```

Each completed stage should be committed before starting the next stage.

---

# 58. Git Ignore

Recommended:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/

data/qdrant/
data/qdrant_token/
```

Generated local vector databases should not normally be committed.

---

# 59. Quick Start

Install:

```powershell
uv sync
```

Ingest:

```powershell
uv run python -m semantic_search_demo.ingest
```

Search:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?"
```

Filtered search:

```powershell
uv run python -m semantic_search_demo.query "What requirements apply to production cloud applications?" --owner "Enterprise Architecture"
```

Evaluate retrieval:

```powershell
uv run python -m semantic_search_demo.evaluate
```

Run API:

```powershell
uv run fastapi dev src/semantic_search_demo/api.py
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 60. Current Learning Outcome

At the end of Stage 11, this project demonstrates:

```text
Enterprise Documents
        |
        v
Multi-Format Parsing
        |
        v
Metadata Enrichment
        |
        v
Token-Aware Chunking
        |
        v
Embeddings
        |
        v
Persistent Vector Index
        |
        v
Metadata-Constrained Retrieval
        |
        v
FastAPI Service
        |
        v
Retrieval Evaluation
        |
        v
Controlled Chunking Experiments
```

This provides the retrieval foundation required for building increasingly sophisticated enterprise RAG systems.

---

# 61. Next Stage

The next stage is:

```text
Stage 12 — Hybrid Search
```

The project will combine:

```text
Semantic / Dense Retrieval
            +
Lexical / Keyword Retrieval
            |
            v
        Fusion Ranking
```

The resulting hybrid retriever will then be evaluated against the current dense-only baseline before it is promoted as the default retrieval strategy.