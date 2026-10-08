import json
from pathlib import Path


METADATA_FILE = Path(
    "data/document_metadata.json"
)


def load_metadata_registry() -> dict[str, dict[str, str]]:
    if not METADATA_FILE.exists():
        return {}

    with METADATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def get_document_metadata(
    document_id: str,
) -> dict[str, str]:
    registry = load_metadata_registry()

    return registry.get(
        document_id,
        {},
    )