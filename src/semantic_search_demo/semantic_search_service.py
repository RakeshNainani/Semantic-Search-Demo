from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.models import SearchResult
from semantic_search_demo.vector_store import VectorStore


class SemanticSearchService:
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
    ) -> None:
        self.vector_store = vector_store
        self.embedding_service = embedding_service

    def search(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.0,
        filters: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        query_embedding = self.embedding_service.embed(
            [query]
        )[0]

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            min_score=min_score,
            filters=filters,
        )