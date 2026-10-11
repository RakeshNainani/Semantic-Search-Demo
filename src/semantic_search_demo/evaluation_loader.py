import json
from pathlib import Path

from semantic_search_demo.evaluation_models import (
    EvaluationCase,
)
from semantic_search_demo.evaluation_models import (
    EvaluationCase,
    EvidenceEvaluationCase,
)

def load_evaluation_cases(
    path: Path,
) -> list[EvaluationCase]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return [
        EvaluationCase(
            query_id=item["query_id"],
            query=item["query"],
            relevant_chunk_ids=item[
                "relevant_chunk_ids"
            ],
        )
        for item in data
    ]


def load_evidence_evaluation_cases(
    path: Path,
) -> list[EvidenceEvaluationCase]:

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return [
        EvidenceEvaluationCase(
            query_id=item["query_id"],
            query=item["query"],
            evidence_phrases=item[
                "evidence_phrases"
            ],
        )
        for item in data
    ]