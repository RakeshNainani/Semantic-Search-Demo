from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import numpy as np
from qdrant_client import QdrantClient, models

from semantic_search_demo.models import Chunk, SearchResult
from semantic_search_demo.vector_store import VectorStore


class QdrantVectorStore(VectorStore):
    def __init__(
        self,
        path: str | Path = "data/qdrant",
        collection_name: str = "enterprise_documents",
    ) -> None:
        self.client = QdrantClient(
            path=str(path)
        )

        self.collection_name = collection_name

    def _ensure_collection(
        self,
        vector_size: int,
    ) -> None:
        if self.client.collection_exists(
            collection_name=self.collection_name
        ):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def add(
        self,
        chunks: list[Chunk],
        embeddings: np.ndarray,
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunk count and embedding count must match."
            )

        if not chunks:
            return

        vector_size = embeddings.shape[1]

        self._ensure_collection(
            vector_size=vector_size
        )

        points: list[models.PointStruct] = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
            strict=True,
        ):
            point_id = str(
                uuid5(
                    NAMESPACE_URL,
                    chunk.chunk_id,
                )
            )

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "document_id": chunk.document_id,
                        "source": chunk.source,
                        "file_type": chunk.file_type,
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                        **chunk.metadata,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
        min_score: float = 0.0,
        filters: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        query_filter = None

        if filters:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(
                            value=value
                        ),
                    )
                    for key, value in filters.items()
                ]
            )


        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=top_k,
            with_payload=True,
            query_filter=query_filter,
            score_threshold=(
                min_score
                if min_score > 0
                else None
            ),
        )

        results: list[SearchResult] = []

        for point in response.points:
            score = float(point.score)

            payload = point.payload or {}

            results.append(
                SearchResult(
                    chunk_id=str(payload.get("chunk_id", "")),
                    document_id=str(payload.get("document_id", "")),
                    source=str(payload.get("source", "")),
                    score=score,
                    text=str(payload.get("text", "")),
                )
            )

        return results
    
    def close(self) -> None:
        self.client.close()