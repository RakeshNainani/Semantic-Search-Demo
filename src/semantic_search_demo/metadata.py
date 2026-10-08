import re


FIELD_MAP = {
    "organization": "organization",
    "document owner": "document_owner",
    "version": "version",
    "classification": "classification",
    "effective date": "effective_date",
}


def extract_metadata(
    text: str,
) -> dict[str, str]:
    metadata: dict[str, str] = {}

    # Metadata normally occurs near the beginning.
    lines = text.splitlines()[:30]

    for raw_line in lines:
        line = raw_line.replace("**", "").strip()

        match = re.match(
            r"^([^:]+):\s*(.+)$",
            line,
        )

        if not match:
            continue

        raw_key = match.group(1).strip().lower()
        value = match.group(2).strip()

        key = FIELD_MAP.get(raw_key)

        if key:
            metadata[key] = value

    return metadata