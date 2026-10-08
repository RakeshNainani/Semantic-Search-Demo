from qdrant_client import QdrantClient


client = QdrantClient(
    path="data/qdrant"
)

try:
    points, _ = client.scroll(
        collection_name="enterprise_documents",
        limit=50,
        with_payload=True,
        with_vectors=False,
    )

    for point in points:
        payload = point.payload or {}

        print("=" * 80)
        print("chunk_id:", payload.get("chunk_id"))
        print("document_id:", payload.get("document_id"))
        print(
            "document_owner:",
            payload.get("document_owner"),
        )
        print(
            "classification:",
            payload.get("classification"),
        )

finally:
    client.close()