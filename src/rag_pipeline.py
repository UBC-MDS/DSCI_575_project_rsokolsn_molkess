import sys
import os
from langchain_core.runnables import RunnablePassthrough, chain
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_groq import ChatGroq

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.semantic import load_vectorstore
from src.prompts import build_prompt

load_dotenv()

def build_semantic_retriever(index_path="data/processed/sampled/faiss_index/", k=5):
    """Builds retriever using semantic vectorstore from semantic information retrieval

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
    vectorstore = load_vectorstore(index_path)
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    return retriever

@chain
def build_context(docs):
    """Formats relevant documents and information for the LLM to use as RAG context

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
    llm = ChatGroq(model="llama-3.1-8b-instant")
    return llm

def build_rag_chain(retriever):
    """Builds the RAG pipeline object using the input retriever, prompt template, context building function, and llm

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
    {
        "context": retriever | build_context,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
    )
    return rag_chain


def main():
    query = "What should I get for my 6th grade niece who loves dinosaurs?"
    retriever = build_semantic_retriever()
    rag_chain = build_rag_chain(retriever)
    answer = rag_chain.invoke(query)
    #print(context[:5000])  # Print the first 1000 characters of the context
    print(answer)


if __name__ == "__main__":
    main()
