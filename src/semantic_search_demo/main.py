from pathlib import Path

from semantic_search_demo.chunker import chunk_documents
from semantic_search_demo.loaders.document_loader import load_documents


DOCUMENT_DIRECTORY = Path("data/docs")


def main() -> None:
    documents = load_documents(
        DOCUMENT_DIRECTORY
    )

    print(f"Documents loaded: {len(documents)}")
    print()

    chunks = chunk_documents(
        documents=documents,
        max_characters=800,
    )

    print(f"Chunks created: {len(chunks)}")
    print()

    for chunk in chunks:
        print(
            f"{chunk.chunk_id} | "
            f"{chunk.file_type} | "
            f"{len(chunk.text)} characters"
        )
print()
print("Sample chunk")
print("-" * 80)

sample_chunk = chunks[0]

print(f"Chunk ID: {sample_chunk.chunk_id}")
print(f"Document ID: {sample_chunk.document_id}")
print(f"Source: {sample_chunk.source}")
print(f"Chunk index: {sample_chunk.chunk_index}")

print()
print(sample_chunk.text)

if __name__ == "__main__":
    main()