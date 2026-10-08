from dataclasses import dataclass


@dataclass
class Document:
    document_id: str
    source: str
    file_type: str
    text: str


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    file_type: str
    chunk_index: int
    text: str

@dataclass
class SearchResult:
    chunk_id: str
    document_id: str
    source: str
    score: float
    text: str