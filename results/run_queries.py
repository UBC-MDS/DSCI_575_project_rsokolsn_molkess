"""Load queries CSV, run each query against BM25 and semantic search, and save results. This script performs Milestone 1: Qualitative Evaluation of Retrieval Methods part 4.2"""

import json
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# Navigate to project root
root = Path(__file__).resolve().parent.parent
os.chdir(root)
sys.path.insert(0, "src")

import pandas as pd

from bm25 import (  # noqa: F401 — needed for pickle
    bm25_search,
    custom_preprocess,
    load_retriever,
)
from semantic import load_vectorstore, semantic_search

CSV_PATH = Path(__file__).resolve().parent / "queries.csv"


def format_results(results):
    """Serialize a list of result dicts to a JSON string for CSV storage."""
    return json.dumps(
        [
            {
                "title": r["title"],
                "author": r["author"],
                "rating": r["rating"],
                "score": round(float(r["score"]), 4),
            }
            for r in results
        ]
    )


def main():
    df = pd.read_csv(CSV_PATH)

    print("Loading retrievers...")
    retriever = load_retriever()
    print("BM25 loaded.")
    vectorstore = load_vectorstore()
    print("Semantic loaded.\n")

    for i, row in df.iterrows():
        query = row["query"]
        print(f"Running query: {query}")

        bm_results = bm25_search(query, k=5, retriever=retriever)
        sem_results = semantic_search(query, k=5, vectorstore=vectorstore)

        df.at[i, "bm25"] = format_results(bm_results)
        df.at[i, "semantic_search"] = format_results(sem_results)

    df.to_csv(CSV_PATH, index=False)
    print(f"\nResults saved to {CSV_PATH}")


if __name__ == "__main__":
    main()
