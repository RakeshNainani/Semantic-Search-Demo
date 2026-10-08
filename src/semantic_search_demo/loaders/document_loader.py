from pathlib import Path

from semantic_search_demo.loaders.docx_loader import load_docx
from semantic_search_demo.loaders.markdown_loader import load_markdown
from semantic_search_demo.loaders.pdf_loader import load_pdf
from semantic_search_demo.models import Document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".md",
}


def load_document(path: Path) -> Document:
    extension = path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(path)

    if extension == ".docx":
        return load_docx(path)

    if extension == ".md":
        return load_markdown(path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )

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