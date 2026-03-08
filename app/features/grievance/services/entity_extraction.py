import re


ISSUE_KEYWORDS = {
    "fertilizer": "Fertilizer Shortage",
    "ration": "Ration Distribution",
    "pension": "Pension Delay",
    "water": "Water Supply",
    "electricity": "Electricity Outage",
    "loan": "Loan Servicing",
    "debt": "Debt Collection",
}

ENTITY_STOPWORDS = {
    "block",
    "reports",
    "report",
    "issue",
    "issues",
    "is",
    "was",
    "has",
    "have",
    "for",
    "with",
    "and",
}


def _extract_by_pattern(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None
    value = match.group(1).strip(" .,:;")
    return value if value else None


def _trim_entity(value: str | None, max_tokens: int = 3) -> str | None:
    if not value:
        return None

    tokens = value.split()
    cleaned = []
    for token in tokens:
        if token.lower() in ENTITY_STOPWORDS:
            break
        cleaned.append(token)
        if len(cleaned) >= max_tokens:
            break

    return " ".join(cleaned) if cleaned else None


def infer_issue(text: str) -> str:
    lower = text.lower()
    for token, label in ISSUE_KEYWORDS.items():
        if token in lower:
            return label
    return "General Complaint"


def extract_entities(complaint_text: str) -> dict:
    text = complaint_text or ""

    village = _extract_by_pattern(
        r"village\s+([A-Za-z0-9\-]+(?:\s+[A-Za-z0-9\-]+){0,2})",
        text,
    )
    block = _extract_by_pattern(
        r"block\s+([A-Za-z0-9\-]+(?:\s+[A-Za-z0-9\-]+){0,2})",
        text,
    )

    official = _extract_by_pattern(
        r"(?:dealer|officer|official|employee)\s+(?:named\s+)?([A-Za-z]+(?:\s+[A-Za-z]+){0,2})",
        text,
    )

    village = _trim_entity(village)
    block = _trim_entity(block)
    official = _trim_entity(official)

    issue = infer_issue(text)

    return {
        "village": village,
        "block": block,
        "official_name": official,
        "issue": issue,
    }
