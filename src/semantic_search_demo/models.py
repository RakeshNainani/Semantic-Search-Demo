from dataclasses import dataclass, field


@dataclass
class Document:
    document_id: str
    source: str
    file_type: str
    text: str
    metadata: dict[str, str] = field(
        default_factory=dict
    )


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    file_type: str
    chunk_index: int
    text: str
    metadata: dict[str, str] = field(
        default_factory=dict
    )


@dataclass
class SearchResult:
    chunk_id: str
    document_id: str
    source: str
    score: float
    text: str