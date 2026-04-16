from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def retrieve_semantic_documents(
    query, index_path="data/processed/sampled/faiss_index/", k=5
):
    vectorstore = FAISS.load_local(
        index_path,
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True,
    )

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
        description = doc.metadata.get("description", "N/A")
        categories = sections[4] if len(sections) > 4 else "N/A"
        features = sections[6] if len(sections) > 6 else "N/A"
        review = sections[7] if len(sections) > 7 else "N/A"
        context += f"Title: {title}\nAuthor: {author}\nRating: {rating}\nCategories: {categories}\nFeatures: {features}\nDescription: {description}\nReview: {review}\n\n"
    return context

def build_llm_pipeline():
    llm = ChatGroq(model="llama-3.1-8b-instant")
    return llm

def main():
    # query = "What are some good books about machine learning?"
    # results = retrieve_semantic_documents(query)
    # context = build_context(results)
    # print(context[:5000])  # Print the first 1000 characters of the context

    return


if __name__ == "__main__":
    main()
