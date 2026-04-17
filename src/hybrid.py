from bm25 import (  # noqa: F401 — custom_preprocess needed for pickle deserialization
    custom_preprocess,
    load_retriever,
)
from rag_pipeline import retrieve_semantic_documents


def bm25_retriever(query, index_path="data/processed/sampled/retriever.pickle", k=5):
    bm25 = load_retriever(index_path)
    bm25.k = k
    result = bm25.invoke(query)
    return result


def reciprocal_rank_fusion(ranked_lists, k_constant=60):
    scores = {}
    doc_map = {}
    for ranked_list in ranked_lists:
        for rank, doc in enumerate(ranked_list):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (k_constant + rank + 1)
            doc_map[key] = doc
    sorted_keys = sorted(scores, key=scores.__getitem__, reverse=True)
    return [doc_map[key] for key in sorted_keys]


def hybrid_retriever(query, index_path="data/processed/sampled/retriever.pickle", k=5):
    bm25_results = bm25_retriever(query, index_path=index_path, k=k)
    semantic_results = retrieve_semantic_documents(query, k=k)
    combined_results = reciprocal_rank_fusion([bm25_results, semantic_results])[:k]
    return combined_results


def main():
    # query = "What are some good books about machine learning?"
    # results = hybrid_retriever(query)
    # context = build_context(results)
    # print(context[:5000])  # Print the first 1000 characters of the context
    return


if __name__ == "__main__":
    main()
