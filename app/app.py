import os
import sys

import streamlit as st

# get the search algorithms
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# Cache the BM25 retriever so it only loads once
@st.cache_resource(show_spinner=False)
def get_retriever():
    return load_retriever()


# Cache the FAISS vectorstore and embedding model so they only load once
@st.cache_resource(show_spinner=False)
def get_vectorstore():
    return load_vectorstore()


@st.cache_resource(show_spinner=False)
def get_llm():
    from src.rag_pipeline import build_llm_pipeline

    return build_llm_pipeline()


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

search_tab, rag_tab = st.tabs(["Search", "RAG"])

with search_tab:
    method = st.radio(
        "Retrieval method", ["BM25 Keyword", "FAISS Semantic"], horizontal=True
    )

    query = st.text_input("What kind of book are you looking for?")

    if query:
        from src.bm25 import bm25_search
        from src.semantic import semantic_search

        st.write(f"Top 5 results for _{query}_ using **{method}** searching")

        if method == "BM25 Keyword":
            retriever = get_retriever()
            results = bm25_search(query, retriever=retriever)
            st.write("Note: a higher BM25 score means a closer keyword match")

        elif method == "FAISS Semantic":
            vectorstore = get_vectorstore()
            results = semantic_search(query, vectorstore=vectorstore)
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
    rag_query = st.text_input("Ask a question about books", key="rag_query")

    if rag_query:
        from src.rag_pipeline import build_context, retrieve_semantic_documents

        with st.spinner("Retrieving documents and generating response..."):
            docs = retrieve_semantic_documents(rag_query)
            context = build_context(docs)

            llm = get_llm()
            prompt = (
                "You are a helpful book recommendation assistant. "
                "Based on the following book information, answer the user's question.\n\n"
                f"Context:\n{context}\n"
                f"Question: {rag_query}\n\n"
                "Answer:"
            )
            response = llm.invoke(prompt)

        st.write(response.content)

        st.subheader("Source Documents")
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
