from semantic_search_demo.models import Chunk, Document


def chunk_document(
    document: Document,
    max_characters: int = 800,
) -> list[Chunk]:
    paragraphs = [
        paragraph.strip()
        for paragraph in document.text.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[Chunk] = []

    current_parts: list[str] = []
    current_length = 0
    chunk_index = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)

        if (
            current_parts
            and current_length + paragraph_length > max_characters
        ):
            chunk_text = "\n\n".join(current_parts)

            chunks.append(
                Chunk(
                    chunk_id=f"{document.document_id}-{chunk_index}",
                    document_id=document.document_id,
                    source=document.source,
                    file_type=document.file_type,
                    chunk_index=chunk_index,
                    text=chunk_text,

                    # IMPORTANT
                    metadata=document.metadata.copy(),
                )
            )

            chunk_index += 1
            current_parts = []
            current_length = 0

        current_parts.append(paragraph)
        current_length += paragraph_length

    # Add final chunk
    if current_parts:
        chunk_text = "\n\n".join(current_parts)

        chunks.append(
            Chunk(
                chunk_id=f"{document.document_id}-{chunk_index}",
                document_id=document.document_id,
                source=document.source,
                file_type=document.file_type,
                chunk_index=chunk_index,
                text=chunk_text,

                # IMPORTANT
                metadata=document.metadata.copy(),
            )
        )

    return chunks


def chunk_documents(
    documents: list[Document],
    max_characters: int = 800,
) -> list[Chunk]:
    chunks: list[Chunk] = []

    for document in documents:
        document_chunks = chunk_document(
            document=document,
            max_characters=max_characters,
        )

        chunks.extend(document_chunks)

    return chunks