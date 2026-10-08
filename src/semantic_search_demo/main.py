from pathlib import Path

from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


DOCUMENT_DIRECTORY = Path("data/docs")


def main() -> None:
    search_service = SemanticSearchService(
        document_directory=DOCUMENT_DIRECTORY,
    )

    print("Building index...")

    search_service.build_index()

    query = (
        "I forgot my password and no longer "
        "have access to my MFA device."
    )

    results = search_service.search(
        query=query,
        top_k=5,
        min_score=0.0,
    )

    print()
    print(f"Query: {query}")
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