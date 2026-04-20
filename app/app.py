import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st


# Cache the BM25 retriever so it only loads once
@st.cache_resource(show_spinner=False)
def get_retriever():
    """Load and cache the BM25 retriever for the lifetime of the Streamlit session."""
    return load_retriever()


# Cache the FAISS vectorstore and embedding model so they only load once
@st.cache_resource(show_spinner=False)
def get_vectorstore():
    """Load and cache the FAISS vectorstore for the lifetime of the Streamlit session."""
    return load_vectorstore()


st.markdown(
    """
    <style>
        [data-testid="stSpinner"] > div { flex-direction: row-reverse; }
        [data-testid="stTextInput"] [data-testid="stWidgetLabel"] p {
            font-size: 1.5rem;
        }
        [data-testid="stRadio"] [data-testid="stWidgetLabel"] p {
            font-size: 1.2rem;
        }
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
        from src.hybrid import hybrid_retriever
        from src.rag_pipeline import build_rag_chain, retrieve_documents
        from src.semantic import load_vectorstore

        get_retriever()
        get_vectorstore()
loading.empty()


def _sync_to_rag():
    """Copy the search tab query into the RAG tab input to keep them in sync."""
    st.session_state.rag_query = st.session_state.search_query


def _sync_to_search():
    """Copy the RAG tab query into the search tab input to keep them in sync."""
    st.session_state.search_query = st.session_state.rag_query


search_tab, rag_tab = st.tabs(["Search", "RAG"])

with search_tab:
    search_query = st.text_input(
        "What kind of book are you looking for?",
        key="search_query",
        on_change=_sync_to_rag,
    )
    method = st.radio(
        "Retrieval method", ["BM25 Keyword", "FAISS Semantic"], horizontal=True
    )

    if search_query:
        from src.bm25 import bm25_search
        from src.semantic import semantic_search

        st.subheader(f"{method} Retriever Results")

        if method == "BM25 Keyword":
            retriever = get_retriever()
            results = bm25_search(search_query, retriever=retriever)
            st.write("Note: a higher BM25 score means a closer keyword match")

        elif method == "FAISS Semantic":
            vectorstore = get_vectorstore()
            results = semantic_search(search_query, vectorstore=vectorstore)
            st.write(
                "Note: FAISS semantic matching uses euclidean distance to score the matches. Thus, a lower score is better"
            )

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
                    st.metric(
                        "Retrieval Score", f"{score:.3f}" if score != "" else "N/A"
                    )
                with col2:
                    if book.get("blurb"):
                        desc = book["blurb"]
                        st.caption(desc[:547] + "..." if len(desc) > 550 else desc)

with rag_tab:
    rag_query = st.text_input(
        "What kind of book are you looking for?",
        key="rag_query",
        on_change=_sync_to_search,
    )

    if rag_query:
        with st.spinner("Retrieving documents and generating response..."):
            retriever = hybrid_retriever
            response = build_rag_chain(retriever).invoke(rag_query)
            docs = retrieve_documents(retriever, rag_query)

        st.subheader("LLM Suggestion")

        st.write(response)

        st.subheader("Hybrid Retriever Results (Source Documents)")
        for doc in docs:
            with st.container(border=True):
                title = doc.metadata.get("title", "N/A")
                author = doc.metadata.get("author", "N/A")
                rating = doc.metadata.get("average_rating", "N/A")
                author_str = f" *by {author}*" if author and author != "N/A" else ""
                st.markdown(f"**{title}**{author_str}")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(
                        "Average Rating",
                        f"{rating} / 5.0" if rating and rating != "N/A" else "N/A",
                    )
                with col2:
                    sections = (
                        doc.page_content.split("§") if "§" in doc.page_content else []
                    )
                    blurb = doc.metadata.get("blurb", "")
                    desc = blurb or (sections[5] if len(sections) > 5 else "")
                    if desc:
                        st.caption(desc[:547] + "..." if len(desc) > 550 else desc)
