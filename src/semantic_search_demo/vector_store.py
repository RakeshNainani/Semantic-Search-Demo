from abc import ABC, abstractmethod

import numpy as np

from semantic_search_demo.models import Chunk, SearchResult


class VectorStore(ABC):

    @abstractmethod
    def add(
        self,
        chunks: list[Chunk],
        embeddings: np.ndarray,
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
        min_score: float = 0.0,
        filters: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        pass