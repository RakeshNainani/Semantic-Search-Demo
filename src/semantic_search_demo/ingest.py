from pathlib import Path

from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.ingestion_service import IngestionService
from semantic_search_demo.qdrant_vector_store import QdrantVectorStore


DOCUMENT_DIRECTORY = Path("data/docs")


def main() -> None:
    embedding_service = EmbeddingService()

    vector_store = QdrantVectorStore(
        path="data/qdrant",
        collection_name="enterprise_documents",
    )

    ingestion_service = IngestionService(
        document_directory=DOCUMENT_DIRECTORY,
        vector_store=vector_store,
        embedding_service=embedding_service,
        max_characters=800,
    )

    print("Starting document ingestion...")

    chunk_count = ingestion_service.ingest()

    print(
        f"Ingestion completed. "
        f"{chunk_count} chunks indexed."
    )


if __name__ == "__main__":
    main()