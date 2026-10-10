from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from semantic_search_demo.api_models import (
    IngestResponse,
    SearchRequest,
    SearchResponse,
    SearchResultResponse,
)
from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.ingestion_service import (
    IngestionService,
)
from semantic_search_demo.qdrant_vector_store import (
    QdrantVectorStore,
)
from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Semantic Search API...")

    embedding_service = EmbeddingService()

    vector_store = QdrantVectorStore(
        path="data/qdrant",
        collection_name="enterprise_documents",
    )

    search_service = SemanticSearchService(
        vector_store=vector_store,
        embedding_service=embedding_service,
    )

    ingestion_service = IngestionService(
        document_directory=Path("data/docs"),
        vector_store=vector_store,
        embedding_service=embedding_service,
        max_characters=800,
    )

    app.state.search_service = search_service
    app.state.ingestion_service = ingestion_service
    app.state.vector_store = vector_store

    print("Semantic Search API ready.")

    yield

    print("Shutting down Semantic Search API...")

    vector_store.close()


app = FastAPI(
    title="Enterprise Semantic Search API",
    description=(
        "Semantic search API for enterprise documents "
        "using SentenceTransformers and Qdrant."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@app.post(
    "/ingest",
    response_model=IngestResponse,
)
def ingest() -> IngestResponse:
    ingestion_service: IngestionService = (
        app.state.ingestion_service
    )

    chunk_count = ingestion_service.ingest()

    return IngestResponse(
        status="completed",
        chunks_indexed=chunk_count,
    )


@app.post(
    "/search",
    response_model=SearchResponse,
)
def search(
    search_request: SearchRequest,
) -> SearchResponse:

    search_service: SemanticSearchService = (
        app.state.search_service
    )

    filters: dict[str, str] | None = None

    if search_request.filters:
        raw_filters = (
            search_request.filters.model_dump(
                exclude_none=True
            )
        )

        filters = {
            key: value.strip()
            for key, value in raw_filters.items()
            if value.strip()
        }

        if not filters:
            filters = None

    search_results = search_service.search(
        query=search_request.query,
        top_k=search_request.top_k,
        min_score=search_request.min_score,
        filters=filters,
    )

    results = [
        SearchResultResponse(
            chunk_id=result.chunk_id,
            document_id=result.document_id,
            source=result.source,
            score=result.score,
            text=result.text,
        )
        for result in search_results
    ]

    return SearchResponse(
        query=search_request.query,
        result_count=len(results),
        results=results,
    )