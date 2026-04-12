import os
import sys

import streamlit as st

# get the search algorithms
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# from src.bm25 import bm25_search, custom_preprocess
# from src.semantic import semantic_search


# Cache the BM25 retriever so it only loads once
@st.cache_resource(show_spinner=False)
def get_retriever():
    return load_retriever()


# Cache the FAISS vectorstore and embedding model so they only load once
@st.cache_resource(show_spinner=False)
def get_vectorstore():
    return load_vectorstore()


st.markdown(
    """
    <style>
        [data-testid="stSpinner"] > div { flex-direction: row-reverse; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Amazon Book Finder")

# Warm up both caches on app load so the first search isn't slow
loading = st.empty()
with loading.container():
    with st.spinner("Loading search indexes. Please wait..."):
        # Importing search functions here to avoid blank screen while importing (if imported at top, they import before the loading message is shown and cause a mostly blank screen for a few seconds)
        from src.bm25 import custom_preprocess, load_retriever
        from src.semantic import load_vectorstore

        get_retriever()
        get_vectorstore()
loading.empty()

method = st.radio("Retrieval method", ["BM25 Keyword", "FAISS Semantic"], horizontal=True)

query = st.text_input("What kind of book are you looking for?")

if query:
    # Importing search functions here to avoid blank screen while importing (if imported at top, they import before the loading message is shown and cause a blank screen for a few seconds)
    from src.bm25 import bm25_search
    from src.semantic import semantic_search

    st.write(f"Top 5 results for _{query}_ using **{method}** searching")

    if method == "BM25 Keyword":
        retriever = get_retriever()
        results = bm25_search(query, retriever=retriever)
        st.write(f"Note: a higher BM25 score means a closer keyword match")

    elif method == "FAISS Semantic":
        vectorstore = get_vectorstore()
        results = semantic_search(query, vectorstore=vectorstore)
        st.write(f"Note: FAISS semantic matching uses euclidean distance to score the matches. Thus, a lower score is better")

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
