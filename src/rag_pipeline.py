"""
Builds and runs the RAG pipeline: semantic retrieval via FAISS followed by
answer generation using a Groq LLM.
"""

import os
import sys

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, chain
from langchain_groq import ChatGroq

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.config import FAISS_INDEX_PATH
from src.prompts import build_prompt
from src.semantic import load_vectorstore

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def main():
    """Run a sample query through the full RAG pipeline and print the result."""
    query = "What should I get for my 6th grade niece who loves dinosaurs?"
    retriever = semantic_retriever()
    rag_chain = build_rag_chain(retriever)
    answer = rag_chain.invoke(query)
    print(answer)


def semantic_retriever(path=FAISS_INDEX_PATH, k=5):
    """Builds retriever using semantic vectorstore from semantic information retrieval.

    Parameters
    ----------
    index_path : str, optional
        Path to semantic index, by default "data/processed/sampled/faiss_index/"
    k : int, optional
        number of items to return via semantic search, by default 5

    Returns
    -------
    LangChain retriever
    """
    vectorstore = load_vectorstore(path)
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    return retriever


def retrieve_documents(retriever, query):
    """Invoke the retriever and return the matching documents for a query.

    Parameters
    ----------
    retriever : LangChain retriever
        A retriever object with an .invoke() method.
    query : str
        The search string to retrieve documents for.

    Returns
    -------
    list of LangChain Document
        The documents returned by the retriever.
    """
    docs = retriever.invoke(query)
    return docs


@chain
def build_context(docs):
    """Formats relevant documents and information for the LLM to use as RAG context.

    Parameters
    ----------
    docs : List of LangChain documents

    Returns
    -------
    str
    """
    context = ""
    for doc in docs:
        title = doc.metadata.get("title", "N/A")
        author = doc.metadata.get("author", "N/A")
        rating = doc.metadata.get("average_rating", "N/A")
        sections = doc.page_content.split("§") if "§" in doc.page_content else []
        description = sections[5][:200] if len(sections) > 5 else "N/A"
        categories = sections[4] if len(sections) > 4 else "N/A"
        features = doc.metadata.get("blurb", "N/A")
        review = sections[7][:200] if len(sections) > 7 else "N/A"
        context += f"Title: {title}\nAuthor: {author}\nRating: {rating}\nCategories: {categories}\nFeatures: {features}\nDescription: {description}\nReview: {review}\n\n"
    return context


def build_llm_pipeline():
    """Instantiate and return the Groq LLM used for answer generation.

    Returns
    -------
    ChatGroq
        A ChatGroq instance using the llama-3.1-8b-instant model.
    """
    llm = ChatGroq(model="llama-3.1-8b-instant")
    return llm


def build_rag_chain(retriever):
    """Builds the RAG pipeline object using the input retriever, prompt template, context building function, and LLM.

    Parameters
    ----------
    retriever : LangChain retriever
        either the semantic or hybrid retriever

    Returns
    -------
    RAG Chain
    """
    llm = build_llm_pipeline()
    prompt = build_prompt()
    rag_chain = (
        {"context": retriever | build_context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


if __name__ == "__main__":
    main()
