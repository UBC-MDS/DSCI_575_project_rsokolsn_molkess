"""
Converts reviews and metadata into tokenized index, tokenizes query, returns keyword matches
"""

import pickle
import re

import nltk
from langchain_community.retrievers import BM25Retriever
from nltk.corpus import stopwords

from src.config import BM25_INDEX_PATH, DOCUMENTS_PATH

# Only download stopwords if not already present, to avoid unnecessary downloads during imports or multiple runs
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


def main():
    """Build and save the BM25 retriever from the documents pickle."""
    build_retriever(DOCUMENTS_PATH, BM25_INDEX_PATH)


def custom_preprocess(text):
    """Lowercase, strip punctuation, and remove English stopwords from text.

    Parameters
    ----------
    text : str
        Raw input text to preprocess.

    Returns
    -------
    list of str
        Tokenized list of filtered, lowercased words.
    """
    stop_words = set(stopwords.words("english"))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = text.split()
    text = [t for t in text if t not in stop_words]
    return text


def load_retriever(retriever_path=BM25_INDEX_PATH):
    """Load a serialized BM25Retriever from disk.

    Parameters
    ----------
    retriever_path : Path
        Path to the pickled BM25Retriever file.

    Returns
    -------
    BM25Retriever
        The deserialized retriever, ready for search.
    """
    with open(retriever_path, "rb") as f:
        return pickle.load(f)


def build_retriever(doc_path, retriever_path):
    """Build a BM25Retriever from a documents pickle and save it to disk.

    Parameters
    ----------
    doc_path : Path
        Path to the pickle file containing LangChain Document objects.
    retriever_path : Path
        Path where the serialized BM25Retriever will be saved.
    """
    with open(doc_path, "rb") as f:
        docs = pickle.load(f)

    print(f"Loaded {len(docs)} documents from pickle")

    print("Building retriever ...")
    retriever = BM25Retriever.from_documents(docs, preprocess_func=custom_preprocess)
    print("Retriever built!")

    with open(retriever_path, "wb") as f:
        pickle.dump(retriever, f)
    print(f"Saved retriever for future use: {retriever_path}")


def bm25_search(query="a book", k=5, retriever=None, retriever_path=BM25_INDEX_PATH):
    """Search the BM25 index and return the top-k matching documents with scores.

    Parameters
    ----------
    query : str
        The search string.
    k : int
        Number of top results to return.
    retriever : BM25Retriever, optional
        A pre-loaded retriever. If None, one is loaded from retriever_path.
    retriever_path : Path
        Path to the pickled retriever. Used only if retriever is None.

    Returns
    -------
    list of dict
        Each dict has keys "title", "author", "rating", "blurb", and "score".
    """
    if retriever is None:
        retriever = load_retriever(retriever_path)

    tokenized_query = custom_preprocess(query)

    # can't use .invoke() if we want to return the scores as well
    scores = retriever.vectorizer.get_scores(tokenized_query)
    top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
        :k
    ]
    results = [(retriever.docs[i], scores[i]) for i in top_k_indices]

    return [
        {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "rating": doc.metadata.get("average_rating", ""),
            "blurb": doc.metadata.get("blurb", ""),
            "score": score,
        }
        for doc, score in results
    ]


if __name__ == "__main__":
    main()
