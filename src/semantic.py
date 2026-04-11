import pickle

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def main():
    """Build the FAISS index. This should be run once after the documents pickle is created. It will load the documents, create the index, and save it to disk."""
    index_path = "data/processed/sampled/faiss_index"
    create_index(index_path=index_path)


def semantic_search(query, k=5, index_path="data/processed/sampled/faiss_index"):
    """Search the FAISS index for documents semantically similar to the query.

    Parameters
    ----------
    query : str
        The search string to embed and match against the index.
    k : int
        Number of top results to return.
    index_path : str
        Path to the saved FAISS index directory.

    Returns
    -------
    list of dict
        Each dict has keys "title", "author", "rating", "review", and "score".
    """
    embeddings = get_embedding_model()
    vectorstore = FAISS.load_local(
        index_path, embeddings, allow_dangerous_deserialization=True
    )
    docs_and_scores = vectorstore.similarity_search_with_score(query, k=k)
    return [
        {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "rating": doc.metadata.get("average_rating", ""),
            "description": doc.metadata.get("description", ""),
            "review": doc.metadata.get("review", ""),
            "score": score,
        }
        for doc, score in docs_and_scores
    ]


def create_index(
    index_path="data/processed/sampled/faiss_index",
    documents_path="data/processed/sampled/documents.pickle",
):
    """Build a FAISS index from the documents pickle and save it to disk.

    Parameters
    ----------
    index_path : str
        Directory path where the FAISS index will be saved.
    documents_path : str
        Path to the pickle file containing LangChain Document objects.
    """
    print("Loading documents...")
    with open(documents_path, "rb") as f:
        documents = pickle.load(f)
    print(f"Loaded {len(documents)} documents.")

    print("Loading embedding model...")
    embeddings = get_embedding_model()

    print("Building FAISS index (this may take a few minutes)...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    print(f"Saving index to {index_path}...")
    vectorstore.save_local(index_path)
    print("Index saved.")


def get_embedding_model():
    """Load and return the HuggingFace sentence transformer embedding model.

    Returns
    -------
    HuggingFaceEmbeddings
        Embedding model wrapper used by LangChain to encode text into vectors.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


if __name__ == "__main__":
    main()
