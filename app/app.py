import os
import sys

import streamlit as st

# get the search algorithms
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.bm25 import bm25_search, load_retriever, custom_preprocess
from src.semantic import semantic_search

# Cache the BM25 retriever so it only loads once
@st.cache_resource
def get_retriever():
    return load_retriever()


st.title("Amazon Book Finder")

method = st.radio("Retrieval method", ["BM25", "Semantic"], horizontal=True)

query = st.text_input("What kind of book are you looking for?")

if query:
    st.write(f"Top 5 results for _{query}_ using **{method}** searching")

    if method == "BM25":
        retriever = get_retriever()
        results = bm25_search(query, retriever=retriever)
    elif method == "Semantic":
        results = semantic_search(query)
    
    if not results:
            st.info("No results found. Try a different query.")

    for i, book in enumerate(results, 1):
        with st.container(border=True):
            author_str = f" *by {book['author']}*" if book["author"] else ""
            st.markdown(f"**{book['title']}**{author_str}")
            col1, col2 = st.columns([1, 3])
            with col1:
                rating = book.get("rating", "")
                st.metric("Average Rating", f"{rating} / 5.0" if rating else "N/A")
                score = book.get("score", "")
                st.metric("Retrieval Score", f"{score:.3f}" if score != "" else "N/A")
            with col2:
                if book.get("description"):
                    st.markdown("**Description:**")
                    st.caption(book["description"])
                if book.get("review"):
                    st.markdown("**Review:**")
                    st.caption(book["review"])
