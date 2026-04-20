"""
Converts reviews and metadata into tokenized and embedded documents ready for search.
"""

import ast
import pickle

import pyarrow.parquet as pq
from langchain_core.documents import Document

from src.config import METADATA_SAMPLE_PATH, REVIEWS_SAMPLE_PATH, SAMPLED_DIR


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


def build_documents_string(file_path, review_df):
    """Create LangChain documents for each book from the meta data. Each document's page_content is sections joined by § in the order: title§subtitle§author§store§categories§description§features§reviews. The metadata contains the parent_asin, title, author, average_rating, and full description.

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
        features = " ".join(row["features"])

        # Sections joined by § so reviews can be re-extracted from page_content.
        # Section order: title§subtitle§author§store§categories§description§features§reviews
        # Expect § to be removed during embedding preprocessing, so it won't interfere with BM25 or semantic search.
        page_content = "§".join(
            [
                row["title"],
                str(row["subtitle"]),
                str(row["author_name"]),
                str(row["store"]),
                " ".join(row["categories"]),
                " ".join(row["description"]),
                features,
                str(row["reviews"]),
            ]
        )

        doc = Document(
            page_content=page_content,
            metadata={
                "parent_asin": row["parent_asin"],
                "title": row["title"],
                "author": row["author_name"],
                "average_rating": row["average_rating"],
                "blurb": features,
            },
        )
        documents.append(doc)

    # Save documents to pickle
    with open(SAMPLED_DIR / "documents.pickle", "wb") as f:
        pickle.dump(documents, f)
    print(f"Saved {len(documents)} documents to {SAMPLED_DIR / 'documents.pickle'}")

    return documents


def main():
    """Aggregate reviews, build LangChain documents, and save them to pickle."""
    reviews = aggregate_reviews(file_path=REVIEWS_SAMPLE_PATH)

    documents = build_documents_string(
        file_path=METADATA_SAMPLE_PATH, review_df=reviews
    )
    print(f"Processed {len(documents)} documents")


if __name__ == "__main__":
    main()
