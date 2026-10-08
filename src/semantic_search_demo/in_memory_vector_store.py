import numpy as np

from semantic_search_demo.models import Chunk, SearchResult
from semantic_search_demo.similarity import cosine_similarity
from semantic_search_demo.vector_store import VectorStore


class InMemoryVectorStore(VectorStore):

    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.embeddings: np.ndarray | None = None

    def add(
        self,
        chunks: list[Chunk],
        embeddings: np.ndarray,
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunk count and embedding count must match."
            )

        self.chunks = chunks
        self.embeddings = embeddings

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
        min_score: float = 0.0,
    ) -> list[SearchResult]:

        if self.embeddings is None:
            raise RuntimeError(
                "Vector store is empty."
            )

        scores = cosine_similarity(
            query_embedding=query_embedding,
            document_embeddings=self.embeddings,
        )

        ranked_indices = np.argsort(scores)[::-1]

        print()
        print("Top raw similarity scores:")
        for index in ranked_indices[:5]:
            print(
                f"{self.chunks[index].chunk_id}: "
                f"{scores[index]:.4f}"
            )


        results: list[SearchResult] = []

        for index in ranked_indices:
            score = float(scores[index])

            if score < min_score:
                continue

            chunk = self.chunks[index]

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