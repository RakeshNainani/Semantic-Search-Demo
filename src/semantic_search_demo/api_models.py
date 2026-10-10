from pydantic import BaseModel, Field


class SearchFilters(BaseModel):
    document_owner: str | None = None
    classification: str | None = None
    file_type: str | None = None


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Natural-language search query.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of results to return.",
    )

    min_score: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Minimum cosine similarity score.",
    )

    filters: SearchFilters | None = None


class SearchResultResponse(BaseModel):
    chunk_id: str
    document_id: str
    source: str
    score: float
    text: str


class SearchResponse(BaseModel):
    query: str
    result_count: int
    results: list[SearchResultResponse]