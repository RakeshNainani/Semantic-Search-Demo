from pathlib import Path

from semantic_search_demo.models import Document


def load_markdown(path: Path) -> Document:
    text = path.read_text(
        encoding="utf-8"
    ).strip()

    return Document(
        document_id=path.stem,
        source=str(path),
        file_type="md",
        text=text,
    )