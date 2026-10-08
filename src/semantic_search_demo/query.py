import argparse

from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.qdrant_vector_store import QdrantVectorStore
from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Semantic search over enterprise documents."
    )

    parser.add_argument(
        "query",
        type=str,
        help="Natural-language search query.",
    )

    parser.add_argument(
        "--owner",
        type=str,
        default=None,
        help="Filter by document owner.",
    )

    parser.add_argument(
        "--classification",
        type=str,
        default=None,
        help="Filter by document classification.",
    )

    parser.add_argument(
        "--file-type",
        type=str,
        default=None,
        help="Filter by file type, for example pdf or docx.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Maximum number of results.",
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="Minimum similarity score.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    embedding_service = EmbeddingService()

    vector_store = QdrantVectorStore(
        path="data/qdrant",
        collection_name="enterprise_documents",
    )

    search_service = SemanticSearchService(
        vector_store=vector_store,
        embedding_service=embedding_service,
    )

    filters: dict[str, str] = {}

    if args.owner:
        filters["document_owner"] = args.owner

    if args.classification:
        filters["classification"] = args.classification

    if args.file_type:
        filters["file_type"] = args.file_type

    results = search_service.search(
        query=args.query,
        top_k=args.top_k,
        min_score=args.min_score,
        filters=filters or None,
    )

    print()
    print(f"Query: {args.query}")

    if filters:
        print(f"Filters: {filters}")

    print()

    if not results:
        print("No relevant results found.")
        return

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Document: {result.document_id}")
        print(f"Chunk: {result.chunk_id}")
        print(f"Source: {result.source}")

        print()
        print(result.text)
        print()


if __name__ == "__main__":
    main()