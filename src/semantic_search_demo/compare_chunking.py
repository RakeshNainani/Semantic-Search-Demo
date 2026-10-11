from pathlib import Path

from semantic_search_demo.embeddings import (
    EmbeddingService,
)
from semantic_search_demo.evaluation_loader import (
    load_evidence_evaluation_cases,
)
from semantic_search_demo.evidence_evaluator import (
    EvidenceEvaluator,
)
from semantic_search_demo.qdrant_vector_store import (
    QdrantVectorStore,
)
from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


EVALUATION_FILE = Path(
    "data/evaluation/chunking_cases.json"
)


def calculate_summary(
    results,
) -> dict[str, float]:

    count = len(results)

    if count == 0:
        return {
            "precision": 0.0,
            "recall": 0.0,
            "hit_rate": 0.0,
            "mrr": 0.0,
        }

    return {
        "precision": sum(
            result.precision_at_k
            for result in results
        ) / count,

        "recall": sum(
            result.evidence_recall_at_k
            for result in results
        ) / count,

        "hit_rate": sum(
            result.hit_rate_at_k
            for result in results
        ) / count,

        "mrr": sum(
            result.reciprocal_rank
            for result in results
        ) / count,
    }


def evaluate_strategy(
    name: str,
    vector_store: QdrantVectorStore,
    embedding_service: EmbeddingService,
    evaluation_cases,
    top_k: int,
) -> dict[str, float]:

    search_service = SemanticSearchService(
        vector_store=vector_store,
        embedding_service=embedding_service,
    )

    evaluator = EvidenceEvaluator(
        search_service=search_service,
    )

    results = evaluator.evaluate(
        evaluation_cases=evaluation_cases,
        top_k=top_k,
    )

    print()
    print("=" * 80)
    print(
        f"{name} — K={top_k}"
    )
    print("=" * 80)

    for result in results:
        print()
        print(
            f"Query ID: {result.query_id}"
        )
        print(
            f"Retrieved: "
            f"{result.retrieved_chunk_ids}"
        )
        print(
            f"Precision@{top_k}: "
            f"{result.precision_at_k:.3f}"
        )
        print(
            f"Evidence Recall@{top_k}: "
            f"{result.evidence_recall_at_k:.3f}"
        )
        print(
            f"Hit Rate@{top_k}: "
            f"{result.hit_rate_at_k:.3f}"
        )
        print(
            f"RR: "
            f"{result.reciprocal_rank:.3f}"
        )

    return calculate_summary(results)

def main() -> None:

    embedding_service = EmbeddingService()

    baseline_store = QdrantVectorStore(
        path="data/qdrant",
        collection_name="enterprise_documents",
    )

    token_store = QdrantVectorStore(
        path="data/qdrant_token",
        collection_name=(
            "enterprise_documents_token_v1"
        ),
    )

    try:
        evaluation_cases = (
            load_evidence_evaluation_cases(
                EVALUATION_FILE
            )
        )

        print()
        print("=" * 80)
        print("CHUNKING STRATEGY COMPARISON")
        print("=" * 80)

        for top_k in [1, 3, 5]:

            baseline = evaluate_strategy(
                name="Baseline Paragraph Chunker",
                vector_store=baseline_store,
                embedding_service=embedding_service,
                evaluation_cases=(
                    evaluation_cases
                ),
                top_k=top_k,
            )

            token = evaluate_strategy(
                name="Token-Aware Chunker",
                vector_store=token_store,
                embedding_service=embedding_service,
                evaluation_cases=(
                    evaluation_cases
                ),
                top_k=top_k,
            )

            print()
            print("-" * 80)
            print(
                f"SUMMARY — K={top_k}"
            )
            print("-" * 80)

            print(
                f"{'Metric':<25}"
                f"{'Baseline':>15}"
                f"{'Token-aware':>15}"
            )

            print(
                f"{'Precision':<25}"
                f"{baseline['precision']:>15.3f}"
                f"{token['precision']:>15.3f}"
            )

            print(
                f"{'Evidence Recall':<25}"
                f"{baseline['recall']:>15.3f}"
                f"{token['recall']:>15.3f}"
            )

            print(
                f"{'Hit Rate':<25}"
                f"{baseline['hit_rate']:>15.3f}"
                f"{token['hit_rate']:>15.3f}"
            )

            print(
                f"{'MRR':<25}"
                f"{baseline['mrr']:>15.3f}"
                f"{token['mrr']:>15.3f}"
            )

    finally:
        baseline_store.close()
        token_store.close()


if __name__ == "__main__":
    main()