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

def build_meta_data_string(file_path, batch_size=10000):
    """create LangChain documents for each book from the meta data

    Parameters
    ----------
    file_path : Path
        Path to the meta_data file
    batch_size : int
        Number of rows to process in each chunk
    """

    pf = pq.ParquetFile(file_path)

    documents = []
    batches = pf.iter_batches(
        batch_size=batch_size, 
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
            ])
    
    num_docs = 0
    for batch in batches:
        df = batch.to_pandas()
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
                )
            doc = Document(
                page_content=page_content,
                metadata={'parent_asin': row['parent_asin'], 'average_rating': row['average_rating']}
            )
            documents.append(doc)

        num_docs += len(documents)
        
        # Save documents to pickle after each chunk
        with open(DATA_DIR / 'meta_data_documents.pickle', 'wb') as f:
            pickle.dump(documents, f)
        print(f'Saved {num_docs} documents to {DATA_DIR / "meta_data_documents.pickle"}')
    

def main(): 
    build_meta_data_string(
        file_path=metadata_path
    )


if __name__ == "__main__":
    main()