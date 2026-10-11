from abc import ABC, abstractmethod

from semantic_search_demo.models import Chunk, Document


class ChunkingStrategy(ABC):

    @abstractmethod
    def chunk_documents(
        self,
        documents: list[Document],
    ) -> list[Chunk]:
        pass