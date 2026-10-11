from pathlib import Path

from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.ingestion_service import IngestionService
from semantic_search_demo.qdrant_vector_store import QdrantVectorStore
from semantic_search_demo.chunker import ParagraphChunker
from semantic_search_demo.token_chunker import TokenAwareChunker


DOCUMENT_DIRECTORY = Path("data/docs")


def main() -> None:
    embedding_service = EmbeddingService()

    vector_store = QdrantVectorStore(
        path="data/qdrant",
        collection_name="enterprise_documents",
    )
    # chunking_strategy = ParagraphChunker(max_characters=800)
    chunking_strategy = TokenAwareChunker(
        tokenizer=embedding_service.tokenizer,
        max_tokens=220,
        overlap_tokens=30,
    )

    ingestion_service = IngestionService(
        document_directory=DOCUMENT_DIRECTORY,
        vector_store=vector_store,
        embedding_service=embedding_service,
        chunking_strategy=chunking_strategy,
    )

    print("Starting document ingestion...")

    chunk_count = ingestion_service.ingest()

    print(
        f"Ingestion completed. "
        f"{chunk_count} chunks indexed."
    )


if __name__ == "__main__":
    main()