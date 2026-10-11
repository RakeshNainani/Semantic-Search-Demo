from pathlib import Path

from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.ingestion_service import IngestionService
from semantic_search_demo.qdrant_vector_store import QdrantVectorStore
from semantic_search_demo.token_chunker import TokenAwareChunker


DOCUMENT_DIRECTORY = Path("data/docs")

def main() -> None:

    embedding_service = EmbeddingService()

    chunking_strategy = TokenAwareChunker(
        tokenizer=embedding_service.tokenizer,
        max_tokens=220,
        overlap_tokens=30,
    )

    vector_store = QdrantVectorStore(
        path="data/qdrant_token",
        collection_name=("enterprise_documents_token_v1"),
    )

    try:
        ingestion_service = IngestionService(
            document_directory=(DOCUMENT_DIRECTORY),
            vector_store=vector_store,
            embedding_service=(embedding_service),
            chunking_strategy=(chunking_strategy),
        )

        print("Starting token-aware ingestion...")

        chunk_count = (ingestion_service.ingest())

        print(
            "Token-aware ingestion completed. "
            f"{chunk_count} chunks indexed."
        )

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()