import os
import sys

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.semantic import load_vectorstore

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def retrieve_semantic_documents(
    query, index_path="data/processed/sampled/faiss_index/", k=5
):
    vectorstore = load_vectorstore(index_path)
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    docs = retriever.invoke(query)
    return docs


def build_context(docs):
    context = ""
    for doc in docs:
        title = doc.metadata.get("title", "N/A")
        author = doc.metadata.get("author", "N/A")
        rating = doc.metadata.get("average_rating", "N/A")
        sections = doc.page_content.split("§") if "§" in doc.page_content else []
        description = sections[5] if len(sections) > 5 else "N/A"
        categories = sections[4] if len(sections) > 4 else "N/A"
        features = doc.metadata.get("blurb", "N/A")
        review = sections[7] if len(sections) > 7 else "N/A"
        context += f"Title: {title}\nAuthor: {author}\nRating: {rating}\nCategories: {categories}\nFeatures: {features}\nDescription: {description}\nReview: {review}\n\n"
    return context


def build_llm_pipeline():
    llm = ChatGroq(model="llama-3.1-8b-instant")
    return llm


def main():
    #    query = "What are some good books about machine learning?"
    #    results = retrieve_semantic_documents(query)
    #    context = build_context(results)
    #    print(context[:5000])  # Print the first 1000 characters of the context

    return


if __name__ == "__main__":
    main()
