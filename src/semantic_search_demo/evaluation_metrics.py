def precision_at_k(
    retrieved: list[str],
    relevant: list[str],
) -> float:
    if not retrieved:
        return 0.0

    relevant_set = set(relevant)

    relevant_retrieved = sum(
        1
        for chunk_id in retrieved
        if chunk_id in relevant_set
    )

    return relevant_retrieved / len(retrieved)


def recall_at_k(
    retrieved: list[str],
    relevant: list[str],
) -> float:
    if not relevant:
        return 0.0

    retrieved_set = set(retrieved)

    relevant_found = sum(
        1
        for chunk_id in relevant
        if chunk_id in retrieved_set
    )

    return relevant_found / len(relevant)


def hit_rate(
    retrieved: list[str],
    relevant: list[str],
) -> float:
    relevant_set = set(relevant)

    for chunk_id in retrieved:
        if chunk_id in relevant_set:
            return 1.0

    return 0.0


def reciprocal_rank(
    retrieved: list[str],
    relevant: list[str],
) -> float:
    relevant_set = set(relevant)

    for rank, chunk_id in enumerate(
        retrieved,
        start=1,
    ):
        if chunk_id in relevant_set:
            return 1.0 / rank

    return 0.0