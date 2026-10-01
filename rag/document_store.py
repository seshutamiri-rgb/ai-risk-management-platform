
from typing import Any


# Sample project knowledge for our RAG system.
# These are synthetic examples for development and testing.

PROJECT_DOCUMENTS: list[dict[str, Any]] = [
    {
        "document_id": "DOC-001",
        "title": "Project Risk Management Policy",
        "category": "policy",
        "content": (
            "Project managers should review high and critical risks "
            "during project status meetings. Every risk should have "
            "an assigned owner, a mitigation plan, and a target review "
            "date. Critical risks should be escalated to the project "
            "sponsor for review."
        ),
    },
    {
        "document_id": "DOC-002",
        "title": "Lessons Learned: Integration Delays",
        "category": "lessons_learned",
        "content": (
            "Previous projects experienced integration delays when "
            "external dependencies were not confirmed early. Teams "
            "should identify dependencies, confirm delivery dates with "
            "external teams, and track unresolved blockers during "
            "weekly project reviews."
        ),
    },
    {
        "document_id": "DOC-003",
        "title": "Project Governance Guidelines",
        "category": "governance",
        "content": (
            "Project status reports should distinguish confirmed facts "
            "from assumptions. Decisions, risks, issues, and action "
            "items should be documented. Significant changes to scope, "
            "schedule, or budget require review by the authorized "
            "project stakeholders."
        ),
    },
]


def get_all_documents() -> list[dict[str, Any]]:
    """Return a copy of the sample project documents."""
    return [document.copy() for document in PROJECT_DOCUMENTS]



def search_documents(query: str) -> list[dict[str, Any]]:
    """Return documents ranked by keyword relevance."""
    search_terms = set(query.lower().split())

    if not search_terms:
        return []

    results = []

    for document in PROJECT_DOCUMENTS:
        title_words = set(document["title"].lower().split())
        content_words = set(document["content"].lower().split())

        title_matches = search_terms & title_words
        content_matches = search_terms & content_words

        score = (len(title_matches) * 3) + len(content_matches)

        if score > 0:
            results.append(
                {
                    **document,
                    "relevance_score": score,
                    "matched_terms": sorted(
                        title_matches | content_matches
                    ),
                }
            )

    return sorted(
        results,
        key=lambda document: document["relevance_score"],
        reverse=True,
    )