from pathlib import Path

from semantic_search_demo.loaders.docx_loader import load_docx
from semantic_search_demo.loaders.markdown_loader import load_markdown
from semantic_search_demo.loaders.pdf_loader import load_pdf
from semantic_search_demo.models import Document
from semantic_search_demo.metadata import extract_metadata
from semantic_search_demo.metadata_loader import (
    get_document_metadata,
)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".md",
}


def load_document(path: Path) -> Document:
    extension = path.suffix.lower()

    if extension == ".pdf":
        document = load_pdf(path)

    elif extension == ".docx":
        document = load_docx(path)

    elif extension == ".md":
        document = load_markdown(path)
    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    document.metadata.update(
        get_document_metadata(
            document.document_id
        )
    )

    return document

def load_documents(directory: Path) -> list[Document]:
    documents: list[Document] = []

    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        document = load_document(path)

        documents.append(document)

    return documents