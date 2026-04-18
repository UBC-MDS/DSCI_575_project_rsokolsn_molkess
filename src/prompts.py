from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
    You are a helpful Amazon assistant to shop for books. 
    Answer the question using ONLY the following context, which contains real book product listings with title, author, average rating, categories, description, features, and reviews.
    If the question can't be answered using the context, say that the information is not available in the data you have access to.
    Answer in 1-3 complete sentences and be concise. Recommend 1 to 2 books and reference specific book titles along with a brief justification. You may quote the description, features, or reviews of the book in your justification.
    """

# SYSTEM_PROMPT = """
#     You are a helpful Amazon assistant to shop for books.
#     Answer the question using ONLY the following context.
#     If the question can't be answered using the context, say you don't know instead of trying to create an answer.
#     Answer in 1-3 complete sentences and recommend 1 to 2 books. Do not include any information that is not in the context.
#     """

# SYSTEM_PROMPT = """
#     You are an Amazon assistant to shop for books. Using only the context provided, answer the question by recommending 1 to 2 books. If the question can't be answered using the context, say that the information is not available in the data you have access to. Be concise and reference specific book titles along with a brief justification.
#     """


def build_prompt():
    prompt = ChatPromptTemplate.from_template(
        SYSTEM_PROMPT
        + """
Context:
{context}

Question:
{question}

Answer based on the Amazon dataset:
        """
    )
    return prompt
