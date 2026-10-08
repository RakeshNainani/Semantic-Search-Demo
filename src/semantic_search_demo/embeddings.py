import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    def __init__(self) -> None:
        self.model = SentenceTransformer(MODEL_NAME)

    def embed(
        self,
        texts: list[str],
    ) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings