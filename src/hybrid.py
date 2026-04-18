from bm25 import ( 
    custom_preprocess,
    load_retriever,
)
from rag_pipeline import retrieve_semantic_documents, build_semantic_retriever
from langchain_core.runnables import chain



def bm25_retriever(query, index_path="data/processed/sampled/retriever.pickle", k=5):
    """Return the top-k documents for query using BM25 keyword matching.

    Args:
        query: Search string.
        index_path: Path to the pickled BM25Retriever.
        k: Number of documents to return.

    Returns:
        List of LangChain Document objects ranked by BM25 score.
    """
    bm25 = load_retriever(index_path)
    bm25.k = k  # set k after loading since it's serialized without it
    result = bm25.invoke(query)
    return result


def reciprocal_rank_fusion(ranked_lists, k_constant=60):
    """Merge multiple ranked document lists into one using Reciprocal Rank Fusion.

    Each document is scored as sum(1 / (k_constant + rank + 1)) across all lists
    it appears in. k_constant=60 is the standard default from the original RRF paper.

    Args:
        ranked_lists: List of ranked document lists (each a list of LangChain Documents).
        k_constant: Smoothing constant that dampens the impact of high ranks.

    Returns:
        Deduplicated list of Documents sorted by descending RRF score.
    """
    scores = {}
    doc_map = {}
    for ranked_list in ranked_lists:
        for rank, doc in enumerate(ranked_list):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (k_constant + rank + 1)
            doc_map[key] = doc  # keep reference for reconstruction after sorting
    sorted_keys = sorted(scores, key=scores.__getitem__, reverse=True)
    return [doc_map[key] for key in sorted_keys]

@chain
def hybrid_retriever(
        query):
    """Retrieve the top-k documents by combining BM25 and semantic search via RRF.

    Runs both retrievers independently with k candidates each, then fuses the
    results with reciprocal_rank_fusion and returns the top-k documents.

    Args:
        query: Search string.

    Returns:
        List of LangChain Document objects ranked by RRF score.
    """
    bm25_results = bm25_retriever(query, k=5)
    semantic_retriever = build_semantic_retriever( k=5)
    semantic_results = retrieve_semantic_documents(semantic_retriever, query)
    combined_results = reciprocal_rank_fusion([bm25_results, semantic_results])[:5]
    return combined_results

def main():
    from rag_pipeline import build_rag_chain 

    query = "What are some good books about machine learning?"
    rag_chain = build_rag_chain(hybrid_retriever)
    answer = rag_chain.invoke(query)
    print(answer)
    
    return


if __name__ == "__main__":
    main()
