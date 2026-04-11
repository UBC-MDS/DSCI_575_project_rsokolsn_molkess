"""
Converts reviews and metadata into tokenized and embedded documents ready for search
"""

import ast
import pickle
import re
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from langchain_core.documents import Document

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
    df = pq.read_table(file_path, columns=["title", "text", "parent_asin"]).to_pandas()

    print(f"Total reviews : {len(df)}")

    df["reviews"] = df["title"] + " " + df["text"]
    first_review = (
        df.groupby("parent_asin")["text"]
        .first()
        .reset_index()
        .rename(columns={"text": "first_review"})
    )
    all_reviews = df.groupby("parent_asin")["reviews"].apply(" ".join).reset_index()
    df = all_reviews.merge(first_review, on="parent_asin")

    print(f"Number of reviewed books : {len(df)}")

    return df


def _extract_author_name(author):
    """Extract a plain author name string from the raw author field.

    The author field in the raw data is a stringified Python dict or list of
    dicts (e.g. "{'name': 'Jane Smith', 'avatar': '...'}"). This function
    parses the string and returns just the name(s). If multiple authors are
    present, their names are joined with a comma.

    Parameters
    ----------
    author : str
        Raw author value from the metadata parquet file.

    Returns
    -------
    str
        The author name(s), or an empty string if extraction fails.
    """
    if not isinstance(author, str):
        return ""
    try:
        parsed = ast.literal_eval(author)
        if isinstance(parsed, dict):
            return parsed.get("name", "")
        if isinstance(parsed, list):
            names = [a.get("name", "") for a in parsed if isinstance(a, dict)]
            return ", ".join(n for n in names if n)
    except (ValueError, SyntaxError):
        return author
    return ""


def build_documents_string(file_path, review_df, snippet_length=200):
    """Create LangChain documents for each book from the meta data. Each document's page_content is a concatenation of the title, subtitle, author, store, description, features, categories, and reviews. The metadata contains the parent_asin, title, author, average_rating, a snippet of the description, and a snippet of the first review.

    Parameters
    ----------
    file_path : Path
        Path to the meta_data file
    review_df : pandas DataFrame
        DataFrame of the reviews aggregated by parent_asin
    snippet_length : int
        Number of characters to include in the description and review snippets in the metadata
    """

    df = pq.read_table(
        file_path,
        columns=[
            "title",
            "subtitle",
            "author",
            "parent_asin",
            "average_rating",
            "store",
            "description",
            "features",
            "categories",
        ],
    ).to_pandas()

    df = df.merge(review_df, on="parent_asin", how="left")
    df["author_name"] = df["author"].apply(_extract_author_name)

    documents = []

    for index, row in df.iterrows():
        page_content = (
            row["title"]
            + " "
            + str(row["subtitle"])
            + " "
            + str(row["author_name"])
            + " "
            + str(row["store"])
            + " "
            + " ".join(row["categories"])
            + " "
            + " ".join(row["description"])
            + " "
            + " ".join(row["features"])
            + " "
            + str(row["reviews"])
        )

        first_review = str(row["first_review"]) if pd.notna(row["first_review"]) else ""

        review = (
            first_review[:snippet_length] + "..."
            if len(first_review) > snippet_length
            else first_review
        )

        description_text = (
            " ".join(row["description"]) if len(row["description"]) > 0 else ""
        )

        description = (
            description_text[:snippet_length] + "..."
            if len(description_text) > snippet_length
            else description_text
        )

        doc = Document(
            page_content=page_content,
            metadata={
                "parent_asin": row["parent_asin"],
                "title": row["title"],
                "author": row["author_name"],
                "average_rating": row["average_rating"],
                "review": review,
                "description": description,
            },
        )
        documents.append(doc)

    # Save documents to pickle
    with open(DATA_DIR / "documents.pickle", "wb") as f:
        pickle.dump(documents, f)
    print(f"Saved {len(documents)} documents to {DATA_DIR / 'documents.pickle'}")

    return documents


def main():
    reviews = aggregate_reviews(file_path=reviews_path)

    documents = build_documents_string(file_path=metadata_path, review_df=reviews)
    print(f"Processed {len(documents)} documents")


if __name__ == "__main__":
    main()
