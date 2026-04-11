import os
import sys

import streamlit as st

# get the search algorithms
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import src.bm25
from src.semantic import semantic_search

st.title("Amazon Book Finder")

method = st.radio("Retrieval method", ["BM25", "Semantic"], horizontal=True)

query = st.text_input("What kind of book are you looking for?")

if query:
    st.write(f"Top 5 results for _{query}_ using **{method}** searching")

    # Here we will have the logic to actually run the search based on the method and query above the commented code here is just dummy code for now
    # if method == 'BM25':
    #     books = bm25(query)
    # elif method == 'Semantic':
    #     books == semantic

    if method == "BM25":
        st.warning("BM25 search is not implemented yet. Showing dummy results.")
        results = [
            {
                "title": "Book Title 1",
                "author": "Author A",
                "rating": 4.5,
                "score": 0.75,
                "description": "Example description of the book.",
                "review": "Example review snippet of the book.",
            },
            {
                "title": "Book Title 2",
                "author": "Author B",
                "rating": 4.0,
                "score": 0.60,
                "description": "Example description of the book.",
                "review": "Example review snippet of the book.",
            },
            {
                "title": "Book Title 3",
                "author": "Author C",
                "rating": 4.2,
                "score": 0.55,
                "description": "Example description of the book.",
                "review": "Example review snippet of the book.",
            },
            {
                "title": "Book Title 4",
                "author": "Author D",
                "rating": 4.8,
                "score": 0.30,
                "description": "Example description of the book.",
                "review": "Example review snippet of the book.",
            },
            {
                "title": "Book Title 5",
                "author": "Author E",
                "rating": 2.5,
                "score": 0.26,
                "description": "Example description of the book.",
                "review": "Example review snippet of the book.",
            },
        ]
    elif method == "Semantic":
        results = semantic_search(query)
        if not results:
            st.info("No results found. Try a different query.")

    for i, book in enumerate(results, 1):
        with st.container(border=True):
            author_str = f" *by {book['author']}*" if book.get("author") else ""
            st.markdown(f"**{book['title']}**{author_str}")
            col1, col2 = st.columns([1, 3])
            with col1:
                rating = book.get("rating", "")
                st.metric("Average Rating", f"{rating} / 5" if rating else "N/A")
                score = book.get("score", "")
                st.metric("Retrieval Score", f"{score:.3f}" if score != "" else "N/A")
            with col2:
                if book.get("description"):
                    st.markdown("**Description:**")
                    st.caption(book["description"])
                if book.get("review"):
                    st.markdown("**Review:**")
                    st.caption(book["review"])
