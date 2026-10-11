from pathlib import Path

from semantic_search_demo.embeddings import (
    EmbeddingService,
)
from semantic_search_demo.evaluation_loader import (
    load_evaluation_cases,
)
from semantic_search_demo.qdrant_vector_store import (
    QdrantVectorStore,
)
from semantic_search_demo.retrieval_evaluator import (
    RetrievalEvaluator,
)
from semantic_search_demo.semantic_search_service import (
    SemanticSearchService,
)


EVALUATION_FILE = Path(
    "data/evaluation/retrieval_cases.json"
)


def print_summary(
    results,
    top_k: int,
) -> None:
    case_count = len(results)

    if case_count == 0:
        print("No evaluation cases found.")
        return

    mean_precision = sum(
        result.precision_at_k
        for result in results
    ) / case_count

    mean_recall = sum(
        result.recall_at_k
        for result in results
    ) / case_count

    mean_hit_rate = sum(
        result.hit_rate
        for result in results
    ) / case_count

    mean_reciprocal_rank = sum(
        result.reciprocal_rank
        for result in results
    ) / case_count

    print("=" * 80)
    print(f"OVERALL METRICS @ K={top_k}")
    print("=" * 80)

    print(
        f"Mean Precision@{top_k}: "
        f"{mean_precision:.3f}"
    )

    print(
        f"Mean Recall@{top_k}: "
        f"{mean_recall:.3f}"
    )

    print(
        f"Hit Rate@{top_k}: "
        f"{mean_hit_rate:.3f}"
    )

    print(
        f"MRR@{top_k}: "
        f"{mean_reciprocal_rank:.3f}"
    )

    print()


def main() -> None:
    embedding_service = EmbeddingService()

    vector_store = QdrantVectorStore(
        path="data/qdrant",
        collection_name="enterprise_documents",
    )

    try:
        search_service = SemanticSearchService(
            vector_store=vector_store,
            embedding_service=embedding_service,
        )

        evaluator = RetrievalEvaluator(
            search_service=search_service,
        )

        evaluation_cases = load_evaluation_cases(
            EVALUATION_FILE
        )

        for top_k in [1, 3, 5]:
            results = evaluator.evaluate(
                evaluation_cases=evaluation_cases,
                top_k=top_k,
            )

            for result in results:
                print("=" * 80)
                print(
                    f"Query ID: {result.query_id}"
                )
                print(
                    f"Query: {result.query}"
                )
                print(
                    f"Retrieved: "
                    f"{result.retrieved_chunk_ids}"
                )
                print(
                    f"Relevant: "
                    f"{result.relevant_chunk_ids}"
                )
                print(
                    f"Precision@{top_k}: "
                    f"{result.precision_at_k:.3f}"
                )
                print(
                    f"Recall@{top_k}: "
                    f"{result.recall_at_k:.3f}"
                )
                print(
                    f"Hit Rate@{top_k}: "
                    f"{result.hit_rate:.3f}"
                )
                print(
                    f"Reciprocal Rank: "
                    f"{result.reciprocal_rank:.3f}"
                )
                print()

            print_summary(
                results=results,
                top_k=top_k,
            )

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()