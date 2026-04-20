"""
create_sample.py

Creates a sample of the processed Books dataset for use during development and
testing. Run this before testing any downstream scripts or notebooks so they
can use the smaller sample instead of the full dataset.

Process:
    1. Samples 10,000 unique books from books_metadata.parquet.
    2. Filters books_reviews.parquet to all reviews for those books using
       PyArrow filter pushdown, so the two sample files are self-consistent.

Output files:
    - data/processed/sampled/books_metadata_sample.parquet  10,000 sampled books
    - data/processed/sampled/books_reviews_sample.parquet   All reviews for those books

Prerequisites:
    Run src/load_data.py first to generate the full Parquet files.
"""

import random

import pyarrow as pa
import pyarrow.parquet as pq

from src.config import METADATA_SAMPLE_PATH, REVIEWS_SAMPLE_PATH, SAMPLED_DIR

SAMPLE_SIZE = 10_000  # Number of unique books to sample
RANDOM_SEED = 42  # Fixed seed for reproducibility across runs


def sample_parquet(path, n, seed):
    """
    Sample n rows from a Parquet file without loading the full file into memory.

    Reads row group metadata to determine total row count, selects a random
    subset of row indices, then reads only the row groups that contain those
    indices.

    Parameters:
        path: Path to the .parquet file.
        n:    Number of rows to sample.
        seed: Random seed for reproducibility.

    Returns:
        pd.DataFrame: Sampled rows.
    """
    pf = pq.ParquetFile(path)
    total_rows = pf.metadata.num_rows
    print(f"  Full dataset: {total_rows:,} rows")

    rng = random.Random(seed)
    sampled_indices = set(rng.sample(range(total_rows), n))

    # Read row group by row group, keeping only rows whose global index was sampled
    batches = []
    row_offset = 0
    for rg in range(pf.metadata.num_row_groups):
        rg_size = pf.metadata.row_group(rg).num_rows
        local_indices = [
            i - row_offset
            for i in range(row_offset, row_offset + rg_size)
            if i in sampled_indices
        ]
        if local_indices:
            table = pf.read_row_group(rg)
            batches.append(table.take(local_indices))
        row_offset += rg_size

    return pa.concat_tables(batches).to_pandas()


def main():
    """Sample books from the full dataset and save sampled parquet files.

    Reads the full metadata and reviews parquet files, samples SAMPLE_SIZE unique
    books, filters reviews to those books, and writes both to SAMPLED_DIR.
    """
    if not METADATA_SAMPLE_PATH.exists():
        raise FileNotFoundError(
            f"{METADATA_SAMPLE_PATH} not found. Run src/load_data.py."
        )
    if not REVIEWS_SAMPLE_PATH.exists():
        raise FileNotFoundError(
            f"{REVIEWS_SAMPLE_PATH} not found. Run src/load_data.py."
        )

    SAMPLED_DIR.mkdir(parents=True, exist_ok=True)

    # --- Metadata sample ---
    print("Sampling metadata...")
    metadata_sample = sample_parquet(METADATA_SAMPLE_PATH, SAMPLE_SIZE, RANDOM_SEED)
    out_metadata = SAMPLED_DIR / "books_metadata_sample.parquet"
    metadata_sample.to_parquet(out_metadata, index=False)
    print(f"  {len(metadata_sample):,} books saved to {out_metadata}")

    # --- Reviews sample ---
    # Use PyArrow filter pushdown to read only reviews for the sampled books.
    # This avoids loading all 29.5M rows — only row groups containing matching
    # parent_asin values are read from disk.
    sampled_asins = metadata_sample["parent_asin"].unique().tolist()
    print("\nFiltering reviews to sampled books...")
    reviews_sample = pq.read_table(
        REVIEWS_SAMPLE_PATH,
        filters=[("parent_asin", "in", sampled_asins)],
    ).to_pandas()
    out_reviews = SAMPLED_DIR / "books_reviews_sample.parquet"
    reviews_sample.to_parquet(out_reviews, index=False)
    print(f"  {len(reviews_sample):,} reviews saved to {out_reviews}")


if __name__ == "__main__":
    main()
