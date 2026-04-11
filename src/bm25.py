"""
Converts reviews and metadata into tokenized index, tokenizes query, returns keyword matches
"""
from langchain_community.retrievers import BM25Retriever
import pickle
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

documents_path = "data/processed/sampled/documents.pickle"
index_path = "data/processed/sampled/retriever.pickle"

def custom_preprocess(text):

    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = text.split()
    text = [t for t in text if t not in stop_words]
    return text

def build_retriever(doc_path, retriever_path):
   
    with open(doc_path, "rb") as f:
        docs = pickle.load(f)

    print(f'Loaded {len(docs)} documents from pickle')


    print(f'Building retriever ...')
    retriever = BM25Retriever.from_documents(docs, preprocess_func=custom_preprocess)
    print('Retriever built!')

    with open(retriever_path, "wb") as f:
        pickle.dump(retriever, f)
    print(f'Saved retriever for future use: {retriever_path}')

def bm25_search(query='a book', k = 5, retriever_path = index_path):
    
    with open(retriever_path, "rb") as f: 
        retriever = pickle.load(f)

    retriever.k = k
    results = retriever.invoke(query)

    return results


def main():
    build_retriever(documents_path, index_path)


if __name__ == "__main__":
    main()