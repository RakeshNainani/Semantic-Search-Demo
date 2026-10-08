from pathlib import Path

from semantic_search_demo.chunker import chunk_documents
from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.loaders.document_loader import load_documents
from semantic_search_demo.similarity import cosine_similarity


DOCUMENT_DIRECTORY = Path("data/docs")


def main() -> None:
    documents = load_documents(
        DOCUMENT_DIRECTORY
    )

    chunks = chunk_documents(
        documents=documents,
        max_characters=800,
    )

    chunk_texts = [
        chunk.text
        for chunk in chunks
    ]

    embedding_service = EmbeddingService()

    chunk_embeddings = embedding_service.embed(
        chunk_texts
    )

    query = (
        "I forgot my password and no longer "
        "have access to my MFA device."
    )

    query_embedding = embedding_service.embed(
        [query]
    )[0]

    scores = cosine_similarity(
        query_embedding=query_embedding,
        document_embeddings=chunk_embeddings,
    )

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    print()
    print(f"Query: {query}")

    print()
    print(f"Query embedding shape: {query_embedding.shape}")
    print(f"Scores shape: {scores.shape}")

    print()
    print("First 10 similarity scores:")

    for index, score in enumerate(scores[:10]):
        print(
            f"{index}: "
            f"{chunks[index].chunk_id} "
            f"-> {score:.4f}"
        )


if __name__ == "__main__":
    main()