from semantic_search_demo.evaluation_metrics import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from semantic_search_demo.evaluation_models import (
    EvaluationCase,
    QueryEvaluationResult,
)
from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


class RetrievalEvaluator:
    def __init__(
        self,
        search_service: SemanticSearchService,
    ) -> None:
        self.search_service = search_service

    def evaluate_case(
        self,
        evaluation_case: EvaluationCase,
        top_k: int,
    ) -> QueryEvaluationResult:

        results = self.search_service.search(
            query=evaluation_case.query,
            top_k=top_k,
            min_score=0.0,
        )

        retrieved_chunk_ids = [
            result.chunk_id
            for result in results
        ]

        relevant_chunk_ids = (
            evaluation_case.relevant_chunk_ids
        )

        return QueryEvaluationResult(
            query_id=evaluation_case.query_id,
            query=evaluation_case.query,
            retrieved_chunk_ids=retrieved_chunk_ids,
            relevant_chunk_ids=relevant_chunk_ids,
            precision_at_k=precision_at_k(
                retrieved=retrieved_chunk_ids,
                relevant=relevant_chunk_ids,
            ),
            recall_at_k=recall_at_k(
                retrieved=retrieved_chunk_ids,
                relevant=relevant_chunk_ids,
            ),
            hit_rate=hit_rate(
                retrieved=retrieved_chunk_ids,
                relevant=relevant_chunk_ids,
            ),
            reciprocal_rank=reciprocal_rank(
                retrieved=retrieved_chunk_ids,
                relevant=relevant_chunk_ids,
            ),
        )

    
    def evaluate(
        self,
        evaluation_cases: list[EvaluationCase],
        top_k: int,
    ) -> list[QueryEvaluationResult]:

        return [
            self.evaluate_case(
                evaluation_case=evaluation_case,
                top_k=top_k,
            )
            for evaluation_case in evaluation_cases
        ]