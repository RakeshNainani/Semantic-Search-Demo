from pathlib import Path

from pypdf import PdfReader

from semantic_search_demo.models import Document


def load_pdf(path: Path) -> Document:
    reader = PdfReader(path)

    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip())

    document_text = "\n\n".join(pages)

    return Document(
        document_id=path.stem,
        source=str(path),
        file_type="pdf",
        text=document_text,
    )