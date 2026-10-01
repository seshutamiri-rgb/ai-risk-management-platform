
from unittest.mock import patch

import pytest

from rag.semantic_retriever import retrieve_semantic_documents


def test_semantic_retriever_finds_relevant_document():
    results = retrieve_semantic_documents(
        "Why might an external dependency delay delivery?",
        top_k=3,
    )

    assert results
    assert results[0]["document_id"] == "DOC-002"
    assert "similarity_score" in results[0]


def test_semantic_retriever_returns_empty_for_blank_query():
    assert retrieve_semantic_documents("   ") == []


def test_semantic_retriever_rejects_invalid_top_k():
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        retrieve_semantic_documents("integration delays", top_k=0)