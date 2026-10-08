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
        filters: dict[str, str] | None = None,
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

        results: list[SearchResult] = []

        for index in ranked_indices:
            score = float(scores[index])

            if score < min_score:
                continue

            chunk = self.chunks[index]

            # Apply metadata filters
            if filters:
                if not self._matches_filters(
                    chunk=chunk,
                    filters=filters,
                ):
                    continue

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

    def _matches_filters(
        self,
        chunk: Chunk,
        filters: dict[str, str],
    ) -> bool:

        for key, expected_value in filters.items():

            if key == "document_id":
                actual_value = chunk.document_id

            elif key == "file_type":
                actual_value = chunk.file_type

            elif key == "source":
                actual_value = chunk.source

            else:
                actual_value = chunk.metadata.get(key)

            if actual_value != expected_value:
                return False

        return True