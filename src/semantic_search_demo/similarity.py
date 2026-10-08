import numpy as np


def cosine_similarity(
    query_embedding: np.ndarray,
    document_embeddings: np.ndarray,
) -> np.ndarray:
    query_norm = np.linalg.norm(query_embedding)

    document_norms = np.linalg.norm(
        document_embeddings,
        axis=1,
    )

    dot_products = document_embeddings @ query_embedding

    denominator = document_norms * query_norm

    scores = np.divide(
        dot_products,
        denominator,
        out=np.zeros_like(dot_products),
        where=denominator != 0,
    )

    return scores