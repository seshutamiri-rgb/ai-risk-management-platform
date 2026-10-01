
from sentence_transformers import SentenceTransformer, util

from rag.document_store import get_all_documents


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model only when first needed."""
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def retrieve_semantic_documents(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """Retrieve documents ranked by semantic similarity."""
    if not query or not query.strip():
        return []

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    documents = get_all_documents()

    if not documents:
        return []

    model = get_embedding_model()

    document_texts = [
        f"{document['title']}. {document['content']}"
        for document in documents
    ]

    document_embeddings = model.encode(
        document_texts,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    query_embedding = model.encode(
        query.strip(),
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    similarities = util.cos_sim(
        query_embedding,
        document_embeddings,
    )[0]

    ranked_indices = similarities.argsort(
        descending=True
    ).tolist()

    results = []

    for index in ranked_indices[:top_k]:
        document = documents[index].copy()
        document["similarity_score"] = float(similarities[index])
        results.append(document)

    return results