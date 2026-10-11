from dataclasses import dataclass


@dataclass
class EvaluationCase:
    query_id: str
    query: str
    relevant_chunk_ids: list[str]


@dataclass
class QueryEvaluationResult:
    query_id: str
    query: str

    retrieved_chunk_ids: list[str]
    relevant_chunk_ids: list[str]

    precision_at_k: float
    recall_at_k: float
    hit_rate: float
    reciprocal_rank: float