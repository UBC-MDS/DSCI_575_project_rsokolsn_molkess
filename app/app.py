import streamlit as st
import sys
import os

# get the search algorithms
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.bm25
import src.semantic

st.title('Amazon Book Finder')

method = st.radio("Retrieval method", ["BM25", "Semantic"], horizontal=True)

query = st.text_input("What kind of book are you looking for?")

if query:
    st.write(f"Top 5 books for _{query}_ using **{method}**")


    # Here we will have the logic to actually run the search based on the method and query above the commented code here is just dummy code for now
    # if method == 'BM25':
    #     books = bm25(query)
    # elif method == 'Semantic':
    #     books == semantic
 
    results = [
        {"title": 'Book Title 1', "author": "Author A", "description": "200 token version of matching review or description"},
        {"title": "Book Title 2", "author": "Author B", "description": "200 token version of matching review or description."},
        {"title": "Book Title 3", "author": "Author C", "description": "200 token version of matching review or description"},
        {"title": "Book Title 4", "author": "Author D", "description": "200 token version of matching review or description"},
        {"title": "Book Title 5", "author": "Author E", "description": "200 token version of matching review or description"},
    ]
 
    for i, book in enumerate(results, 1):
        with st.container(border=True):
            st.markdown(f"**{i}. {book['title']}** — {book['author']}")
            st.caption(book["description"])
