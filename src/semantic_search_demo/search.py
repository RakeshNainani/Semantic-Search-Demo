import numpy as np

from semantic_search_demo.embeddings import EmbeddingService
from semantic_search_demo.models import Chunk, SearchResult
from semantic_search_demo.similarity import cosine_similarity


def semantic_search(
    query: str,
    chunks: list[Chunk],
    chunk_embeddings: np.ndarray,
    embedding_service: EmbeddingService,
    top_k: int = 3,
    min_score: float = 0.0,
) -> list[SearchResult]:
    query_embedding = embedding_service.embed(
        [query]
    )[0]

    scores = cosine_similarity(
        query_embedding=query_embedding,
        document_embeddings=chunk_embeddings,
    )

    ranked_indices = np.argsort(scores)[::-1]

    results: list[SearchResult] = []

    for index in ranked_indices:
        score = float(scores[index])

        if score < min_score:
            continue

        chunk = chunks[index]

        results.append(
            SearchResult(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                source=chunk.source,
                score=score,
                text=chunk.text,
            )
        )

        if len(results) >= top_k:
            break

    return results