from pathlib import Path

from semantic_search_demo.chunker import chunk_documents
from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.loaders.document_loader import load_documents
from semantic_search_demo.vector_store import VectorStore


class IngestionService:
    def __init__(
        self,
        document_directory: Path,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        max_characters: int = 800,
    ) -> None:
        self.document_directory = document_directory
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.max_characters = max_characters

    def ingest(self) -> int:
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

        return len(chunks)