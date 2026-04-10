"""
Converts reviews and metadata into tokenized and embedded documents ready for search
"""
import re
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from langchain_core.documents import Document
import pickle

# Starting running only with the sample and once it's working try with the full corpus
# DATA_DIR = Path("../data/processed/full")
# reviews_path = DATA_DIR / "books_reviews.parquet"
# metadata_path = DATA_DIR / "books_metadata.parquet"

# # Open file handles — reads only the Parquet footer (schema + row group stats), not any row data.
# reviews_file = pq.ParquetFile(reviews_path)
# metadata_file = pq.ParquetFile(metadata_path)


DATA_DIR = Path("data/processed/sampled")
reviews_path = DATA_DIR / "books_reviews_sample.parquet"
metadata_path = DATA_DIR / "books_metadata_sample.parquet"

def aggregate_reviews(file_path):
    """Aggregates review title and text by product id (parent_asin)

    Parameters
    ----------
    file_path : Path
        Path to reviews file

    Returns
    -------
    Pandas DataFrame
        DF with one row per product, with concatenated reviews
    """
    df = pq.read_table(
        file_path, 
        columns=[
            'title', 
            'text',  
            'parent_asin'
        ]).to_pandas()
    
    print(f'Total reviews : {len(df)}')

    df["reviews"] = df["title"] + " " + df["text"]
    df = df.groupby("parent_asin")["reviews"].apply(" ".join).reset_index()

    print(f'Number of reviewed books : {len(df)}')

    return df


def build_documents_string(file_path, review_df):
    """create LangChain documents for each book from the meta data

    Parameters
    ----------
    file_path : Path
        Path to the meta_data file
    review_df : pandas DataFrame
        DataFrame of the reviews aggregated by parent_asin
    """

    df = pq.read_table(
        file_path, 
        columns=[
            'title', 
            'subtitle', 
            'author', 
            'parent_asin', 
            'average_rating',
            'store',
            'description',
            'features',
            'categories'
        ]).to_pandas()
    
    df = df.merge(review_df, on='parent_asin', how='left')
    
    documents = []
    
    for index, row in df.iterrows():
        page_content = (
            row['title'] 
            + " " 
            + str(row['subtitle']) 
            + " " 
            + str(row["author"]) 
            + " " 
            + str(row['store'])
            + " "
            + " ".join(row['categories'])
            + " "
            + " ".join(row['description'])
            + " "
            + " ".join(row['features'])
            + " "
            + str(row['reviews'])
        )
        doc = Document(
            page_content=page_content,
            metadata={'parent_asin': row['parent_asin'], 'average_rating': row['average_rating']}
        )
        documents.append(doc)

    # Save documents to pickle
    with open(DATA_DIR / 'documents.pickle', 'wb') as f:
        pickle.dump(documents, f)
    print(f'Saved {len(documents)} documents to {DATA_DIR / "documents.pickle"}')
    
    return documents

def main(): 
    reviews = aggregate_reviews(file_path=reviews_path)

    documents = build_documents_string(
        file_path=metadata_path,
        review_df=reviews
    )
    print(f"Processed {len(documents)} documents")

if __name__ == "__main__":
    main()