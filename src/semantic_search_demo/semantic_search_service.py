from pathlib import Path

from semantic_search_demo.chunker import chunk_documents
from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.in_memory_vector_store import (
    InMemoryVectorStore,
)
from semantic_search_demo.loaders.document_loader import (
    load_documents,
)
from semantic_search_demo.models import SearchResult
from semantic_search_demo.vector_store import VectorStore


class SemanticSearchService:

    def __init__(
        self,
        document_directory: Path,
        vector_store: VectorStore | None = None,
        max_characters: int = 800,
    ) -> None:

        self.document_directory = document_directory
        self.max_characters = max_characters

        self.embedding_service = EmbeddingService()

        self.vector_store = (
            vector_store
            if vector_store is not None
            else InMemoryVectorStore()
        )

    def build_index(self) -> None:
        documents = load_documents(
            self.document_directory
        )

        chunks = chunk_documents(
            documents=documents,
            max_characters=self.max_characters,
        )

        chunk_texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = self.embedding_service.embed(
            chunk_texts
        )

        self.vector_store.add(
            chunks=chunks,
            embeddings=embeddings,
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.0,
    ) -> list[SearchResult]:

        query_embedding = self.embedding_service.embed(
            [query]
        )[0]

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            min_score=min_score,
        )