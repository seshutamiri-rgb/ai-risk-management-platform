
from rag.context_builder import build_rag_context
from rag.retriever import retrieve_relevant_documents


def test_retriever_finds_integration_lessons():
    documents = retrieve_relevant_documents("integration delays")

    assert documents
    assert documents[0]["document_id"] == "DOC-002"


def test_context_builder_includes_document_evidence():
    context = build_rag_context("integration delays")

    assert "PROJECT KNOWLEDGE REFERENCES" in context
    assert "DOC-002" in context
    assert "Integration Delays" in context


def test_context_builder_handles_no_matching_documents():
    context = build_rag_context("xyznonexistentterm123")

    assert "No relevant project knowledge documents were found" in context