from semantic_search_demo.evaluation_models import (
    EvidenceEvaluationCase,
    EvidenceEvaluationResult,
)
from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


class EvidenceEvaluator:

    def __init__(
        self,
        search_service: SemanticSearchService,
    ) -> None:
        self.search_service = search_service

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        return " ".join(
            text.lower().split()
        )

    def _contains_evidence(
        self,
        text: str,
        evidence_phrase: str,
    ) -> bool:

        normalized_text = self._normalize(text)

        normalized_evidence = self._normalize(
            evidence_phrase
        )

        return (
            normalized_evidence
            in normalized_text
        )

    def evaluate_case(
        self,
        evaluation_case: EvidenceEvaluationCase,
        top_k: int,
    ) -> EvidenceEvaluationResult:

        results = self.search_service.search(
            query=evaluation_case.query,
            top_k=top_k,
            min_score=0.0,
        )

        retrieved_chunk_ids = [
            result.chunk_id
            for result in results
        ]

        relevant_result_count = 0
        first_relevant_rank: int | None = None

        evidence_found: set[str] = set()

        for rank, result in enumerate(
            results,
            start=1,
        ):
            result_is_relevant = False

            for evidence_phrase in (
                evaluation_case.evidence_phrases
            ):
                if self._contains_evidence(
                    result.text,
                    evidence_phrase,
                ):
                    result_is_relevant = True
                    evidence_found.add(
                        evidence_phrase
                    )

            if result_is_relevant:
                relevant_result_count += 1

                if first_relevant_rank is None:
                    first_relevant_rank = rank

        precision = (
            relevant_result_count / len(results)
            if results
            else 0.0
        )

        evidence_recall = (
            len(evidence_found)
            / len(
                evaluation_case.evidence_phrases
            )
            if evaluation_case.evidence_phrases
            else 0.0
        )

        hit_rate = (
            1.0
            if relevant_result_count > 0
            else 0.0
        )

        reciprocal_rank = (
            1.0 / first_relevant_rank
            if first_relevant_rank
            else 0.0
        )

        return EvidenceEvaluationResult(
            query_id=evaluation_case.query_id,
            query=evaluation_case.query,
            retrieved_chunk_ids=(
                retrieved_chunk_ids
            ),
            precision_at_k=precision,
            evidence_recall_at_k=(
                evidence_recall
            ),
            hit_rate_at_k=hit_rate,
            reciprocal_rank=reciprocal_rank,
        )

    def evaluate(
        self,
        evaluation_cases: list[
            EvidenceEvaluationCase
        ],
        top_k: int,
    ) -> list[EvidenceEvaluationResult]:

        return [
            self.evaluate_case(
                evaluation_case=case,
                top_k=top_k,
            )
            for case in evaluation_cases
        ]