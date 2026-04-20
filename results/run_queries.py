"""Load queries CSV, run each query against BM25 and semantic search, and save results. This script performs Milestone 1: Qualitative Evaluation of Retrieval Methods part 4.2"""

import json
import os
import sys
import warnings
from dotenv import load_dotenv
from pathlib import Path

warnings.filterwarnings("ignore")

# Navigate to project root
root = Path(__file__).resolve().parent.parent
os.chdir(root)
sys.path.insert(0, "src")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.prompts import build_prompt
from src.semantic import load_vectorstore

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

import pandas as pd

from bm25 import (  
    bm25_search,
    custom_preprocess,
    load_retriever,
)
from semantic import load_vectorstore, semantic_search
from src.hybrid import hybrid_retriever
from src.rag_pipeline import build_rag_chain

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
    """Run all queries from the CSV through BM25, semantic search, and RAG, and save results.

    Loads queries.csv, runs each query through all three retrieval methods, writes
    results back to the same CSV file.
    """
    df = pd.read_csv(CSV_PATH)

    print("Loading retrievers...")
    retriever = load_retriever()
    print("BM25 loaded.")
    vectorstore = load_vectorstore()
    print("Semantic loaded.\n")
    hybr_retriever = hybrid_retriever

    for i, row in df.iterrows():
        query = row["query"]
        print(f"Running query: {query}")

        bm_results = bm25_search(query, k=5, retriever=retriever)
        sem_results = semantic_search(query, k=5, vectorstore=vectorstore)
        hyrbid_rag = build_rag_chain(hybr_retriever).invoke(query)


        df.at[i, "bm25"] = format_results(bm_results)
        df.at[i, "semantic_search"] = format_results(sem_results)
        df.at[i, "hybrid rag"] = hyrbid_rag

    df.to_csv(CSV_PATH, index=False)
    print(f"\nResults saved to {CSV_PATH}")


if __name__ == "__main__":
    main()
