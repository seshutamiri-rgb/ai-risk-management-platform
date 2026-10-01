
from rag.document_store import search_documents


def retrieve_relevant_documents(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Retrieve the most relevant project knowledge documents.

    Args:
        query: The project manager's question.
        top_k: Maximum number of documents to return.

    Returns:
        Relevant documents ordered by keyword relevance.
    """
    if not query or not query.strip():
        return []

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    results = search_documents(query.strip())

    return results[:top_k]