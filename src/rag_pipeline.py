from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def retrieve_documents(query, vectorstore, k=5):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    # Use in a chain
    docs = retriever.invoke(query)
    return docs


def main():
    index_path = "data/processed/sampled/faiss_index/"
    vectorstore = FAISS.load_local(
        index_path,
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True,
    )
    query = "What are some good books about machine learning?"
    results = retrieve_documents(query, vectorstore)
    for i, doc in enumerate(results):
        print(f"Result {i + 1}:")
        print(f"Title: {doc.metadata.get('title', 'N/A')}")
        print(f"Author: {doc.metadata.get('author', 'N/A')}")
        print(f"Rating: {doc.metadata.get('average_rating', 'N/A')}")
        print(f"Description: {doc.metadata.get('description', 'N/A')}")
        print(f"Review: {doc.metadata.get('review', 'N/A')}")
        print("-" * 40)
    return


if __name__ == "__main__":
    main()
