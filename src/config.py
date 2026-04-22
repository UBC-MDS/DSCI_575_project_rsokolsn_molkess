"""
Configuration file for the project, containing constants and paths used across the codebase."""

from pathlib import Path

DATA_DIR = Path(
    "data/processed/"
)  # Directory containing the original full Parquet files
FULL_DIR = DATA_DIR / "full"  # Directory for the full processed Parquet files
SPLITS_DIR = DATA_DIR / "splits"  # Directory for train/val/test split Parquet files
SAMPLED_DIR = (
    DATA_DIR / "sampled"
)  # Directory for the sampled Parquet files and derived artifacts
REVIEWS_SAMPLE_PATH = SAMPLED_DIR / "books_reviews_sample.parquet"
METADATA_SAMPLE_PATH = SAMPLED_DIR / "books_metadata_sample.parquet"
FAISS_INDEX_PATH = SAMPLED_DIR / "faiss_index"
DOCUMENTS_PATH = SAMPLED_DIR / "documents.pickle"
BM25_INDEX_PATH = SAMPLED_DIR / "retriever.pickle"
