import re

from semantic_search_demo.chunking_strategy import (
    ChunkingStrategy,
)
from semantic_search_demo.models import (
    Chunk,
    Document,
)


class TokenAwareChunker(ChunkingStrategy):

    def __init__(
        self,
        tokenizer,
        max_tokens: int = 220,
        overlap_tokens: int = 30,
    ) -> None:

        if max_tokens <= 0:
            raise ValueError(
                "max_tokens must be greater than zero."
            )

        if overlap_tokens < 0:
            raise ValueError(
                "overlap_tokens cannot be negative."
            )

        if overlap_tokens >= max_tokens:
            raise ValueError(
                "overlap_tokens must be smaller "
                "than max_tokens."
            )

        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens

    def _token_count(
        self,
        text: str,
    ) -> int:
        return len(
            self.tokenizer.tokenize(text)
        )

    def _split_large_text(
        self,
        text: str,
    ) -> list[str]:

        tokens = self.tokenizer.tokenize(text)

        pieces: list[str] = []

        for start in range(
            0,
            len(tokens),
            self.max_tokens,
        ):
            token_slice = tokens[
                start:start + self.max_tokens
            ]

            piece = (
                self.tokenizer
                .convert_tokens_to_string(
                    token_slice
                )
                .strip()
            )

            if piece:
                pieces.append(piece)

        return pieces

    def _split_paragraph(
        self,
        paragraph: str,
    ) -> list[str]:

        if self._token_count(paragraph) <= self.max_tokens:
            return [paragraph]

        sentences = re.split(
            r"(?<=[.!?])\s+",
            paragraph,
        )

        pieces: list[str] = []
        current_sentences: list[str] = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            if self._token_count(sentence) > self.max_tokens:

                if current_sentences:
                    pieces.append(
                        " ".join(current_sentences)
                    )

                    current_sentences = []

                pieces.extend(
                    self._split_large_text(sentence)
                )

                continue

            candidate = " ".join(
                current_sentences + [sentence]
            )

            if (
                current_sentences
                and self._token_count(candidate)
                > self.max_tokens
            ):
                pieces.append(
                    " ".join(current_sentences)
                )

                current_sentences = [sentence]

            else:
                current_sentences.append(sentence)

        if current_sentences:
            pieces.append(
                " ".join(current_sentences)
            )

        return pieces

    def _create_overlap(
        self,
        text: str,
        available_tokens: int,
    ) -> str:

        overlap_size = min(
            self.overlap_tokens,
            available_tokens,
        )

        if overlap_size <= 0:
            return ""

        tokens = self.tokenizer.tokenize(text)

        overlap_tokens = tokens[
            -overlap_size:
        ]

        return (
            self.tokenizer
            .convert_tokens_to_string(
                overlap_tokens
            )
            .strip()
        )


    def chunk_document(
        self,
        document: Document,
    ) -> list[Chunk]:

        paragraphs = [
            paragraph.strip()
            for paragraph
            in document.text.split("\n\n")
            if paragraph.strip()
        ]

        units: list[str] = []

        for paragraph in paragraphs:
            units.extend(
                self._split_paragraph(paragraph)
            )

        chunks: list[Chunk] = []

        current_parts: list[str] = []
        chunk_index = 0

        for unit in units:

            candidate_parts = (
                current_parts + [unit]
            )

            candidate_text = "\n\n".join(
                candidate_parts
            )

            if (
                current_parts
                and self._token_count(candidate_text)
                > self.max_tokens
            ):

                chunk_text = "\n\n".join(
                    current_parts
                )

                chunks.append(
                    Chunk(
                        chunk_id=(
                            f"{document.document_id}-"
                            f"{chunk_index}"
                        ),
                        document_id=document.document_id,
                        source=document.source,
                        file_type=document.file_type,
                        chunk_index=chunk_index,
                        text=chunk_text,
                        metadata={
                            **document.metadata,
                            "chunking_strategy":
                                "token_aware_v1",
                        },
                    )
                )

                chunk_index += 1

                unit_tokens = self._token_count(
                    unit
                )

                available_overlap = (
                    self.max_tokens
                    - unit_tokens
                )

                overlap_text = self._create_overlap(
                    text=chunk_text,
                    available_tokens=(
                        available_overlap
                    ),
                )

                current_parts = []

                if overlap_text:
                    current_parts.append(
                        overlap_text
                    )

                current_parts.append(unit)

            else:
                current_parts.append(unit)

        if current_parts:

            chunk_text = "\n\n".join(
                current_parts
            )

            chunks.append(
                Chunk(
                    chunk_id=(
                        f"{document.document_id}-"
                        f"{chunk_index}"
                    ),
                    document_id=document.document_id,
                    source=document.source,
                    file_type=document.file_type,
                    chunk_index=chunk_index,
                    text=chunk_text,
                    metadata={
                        **document.metadata,
                        "chunking_strategy":
                            "token_aware_v1",
                    },
                )
            )

        return chunks

    def chunk_documents(
        self,
        documents: list[Document],
    ) -> list[Chunk]:

        chunks: list[Chunk] = []

        for document in documents:

            chunks.extend(
                self.chunk_document(
                    document=document
                )
            )

        return chunks