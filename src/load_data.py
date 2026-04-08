"""
load_data.py

Streams Amazon Reviews 2023 (Books) data from HuggingFace and saves it locally
as Parquet files.

Output files:
  - data/processed/full/books_reviews.parquet       Full review text and ratings (29.5M rows)
  - data/processed/full/books_metadata.parquet      Book-level metadata (4.4M rows)
  - data/processed/splits/books_splits_train.parquet  Pre-defined train split: IDs + ratings only
  - data/processed/splits/books_splits_valid.parquet  Pre-defined validation split: IDs + ratings only
  - data/processed/splits/books_splits_test.parquet   Pre-defined test split: IDs + ratings only

Join key: all files share `parent_asin` as the canonical book identifier.
"""

from itertools import islice
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from datasets import load_dataset

DATASET_NAME = "McAuley-Lab/Amazon-Reviews-2023"
FULL_DIR = Path("data/processed/full")
SPLITS_DIR = Path("data/processed/splits")
BATCH_SIZE = 100_000  # Number of records to hold in memory at once before writing

# Configs loaded with split="full" (no pre-defined train/valid/test split).
# drop_cols: fields excluded from the output Parquet file.
#   - "images": lists of image URLs
#   - "videos": dicts of video URLs
FULL_SOURCES = [
    {
        "config": "raw_review_Books",
        "output": "books_reviews.parquet",
        "drop_cols": {"images"},
    },
    {
        "config": "raw_meta_Books",
        "output": "books_metadata.parquet",
        "drop_cols": {"images", "videos"},
    },
]

# Pre-split config: contains only IDs + ratings (no review text), split by
# timestamp so that train interactions are older than valid/test. Used to define
# which (user_id, parent_asin) pairs belong to each evaluation partition.
SPLIT_CONFIG = "0core_timestamp_Books"
SPLIT_NAMES = ["train", "valid", "test"]


def iter_batches(iterable, batch_size):
    """
    Yield successive fixed-size batches from an iterable.

    Used to accumulate records from a streaming HuggingFace dataset before
    writing to Parquet.

    Parameters:
        iterable:   A HuggingFace IterableDataset, though can be any iterable.
        batch_size: Number of records per batch.

    Yields:
        list: A batch of up to `batch_size` records. The final batch may be
              smaller if the total number of records is not evenly divisible.
    """
    it = iter(iterable)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch


def stream_to_parquet(config, split, output_path, drop_cols):
    """
    Stream a single HuggingFace dataset config/split and write it to Parquet.

    Process:
        1. Opens a streaming connection to HuggingFace.
        2. Iterates records in batches of BATCH_SIZE.
        3. Drops unwanted columns from each batch.
        4. Infers the Parquet schema from the first batch, then appends
           subsequent batches to the same file using a single ParquetWriter.
        5. Closes the writer when all records are processed.

    The Parquet file uses Snappy compression, which gives a good balance of
    file size reduction and read/write speed.

    Parameters:
        config:      HuggingFace dataset config name (e.g. "raw_review_Books").
        split:       Dataset split to load (e.g. "full", "train", "valid", "test").
        output_path: Path object for the output .parquet file.
        drop_cols:   Set of column names to exclude from the output.
    """
    print(f"\nStreaming {config} ({split})...")
    ds = load_dataset(
        DATASET_NAME,
        config,
        split=split,
        streaming=True,  # Fetch records on demand instead of downloading all at once
        trust_remote_code=True,  # Required: this dataset uses a custom loading script
    )

    writer = None  # Initialised on first batch so schema can be inferred from data
    total = 0

    for batch in iter_batches(ds, BATCH_SIZE):
        # Remove unwanted columns from every record in the batch
        records = [{k: v for k, v in r.items() if k not in drop_cols} for r in batch]

        # Convert the list of dicts to a PyArrow Table for Parquet writing
        table = pa.Table.from_pylist(records)

        if writer is None:
            # Open the writer on the first batch so the schema is derived from
            # actual data rather than guessed upfront
            writer = pq.ParquetWriter(output_path, table.schema, compression="snappy")

        writer.write_table(table)
        total += len(batch)
        print(f"  written {total:,} records", end="\r")

    if writer:
        writer.close()

    print(f"\n  done. {total:,} records saved to {output_path}")


def main():
    """
    Load all required dataset configs and write them to Parquet.

    Execution order:
        1. books_reviews.parquet    -- full review text, largest file (~29.5M rows)
        2. books_metadata.parquet   -- book-level metadata (~4.4M rows)
        3. books_splits_train/valid/test.parquet -- ID-only interaction splits
    """
    FULL_DIR.mkdir(parents=True, exist_ok=True)
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)

    # Stream full (unsplit) configs: reviews and metadata
    for source in FULL_SOURCES:
        stream_to_parquet(
            config=source["config"],
            split="full",
            output_path=FULL_DIR / source["output"],
            drop_cols=source["drop_cols"],
        )

    # Stream the pre-defined temporal splits (IDs + ratings only, no text)
    for split in SPLIT_NAMES:
        stream_to_parquet(
            config=SPLIT_CONFIG,
            split=split,
            output_path=SPLITS_DIR / f"books_splits_{split}.parquet",
            drop_cols=set(),  # Keep all columns; this config has no cols to drop
        )


if __name__ == "__main__":
    main()
