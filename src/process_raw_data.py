"""
process_raw_data.py

Processes locally downloaded Amazon Reviews 2023 (Books) raw files into Parquet.
Use this script if you downloaded the raw files manually instead of streaming
them from HuggingFace via load_data.py.

Expected input files in data/raw/:
  - Books.jsonl.gz        Review text and ratings (29.5M rows)
  - meta_Books.jsonl.gz   Book-level metadata (4.4M rows)

Output files:
  - data/processed/full/books_reviews.parquet     Same schema as produced by load_data.py
  - data/processed/full/books_metadata.parquet    Same schema as produced by load_data.py

Join key: both files share `parent_asin` as the canonical book identifier.
"""

import gzip
import json
from itertools import islice
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed/full")
BATCH_SIZE = 100_000  # Number of records to hold in memory at once before writing

SOURCES = [
    {
        "input": "Books.jsonl.gz",
        "output": "books_reviews.parquet",
        "drop_cols": {"images"},  # Lists of image URLs
    },
    {
        "input": "meta_Books.jsonl.gz",
        "output": "books_metadata.parquet",
        "drop_cols": {"images", "videos"},  # URL fields
    },
]


def iter_batches(iterable, batch_size):
    """
    Yield successive fixed-size batches from an iterable.

    Used to accumulate records from a .jsonl.gz file before writing to Parquet.

    Parameters:
        iterable:   Any iterable, typically a generator of parsed JSON lines.
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


def iter_jsonl_gz(file_path):
    """
    Yield parsed JSON records from a gzipped JSONL file, one line at a time.

    Each line in the file is a self-contained JSON object. Yields one dict per
    line. Skips blank lines silently.

    Parameters:
        file_path: Path object pointing to a .jsonl.gz file.

    Yields:
        dict: A single parsed JSON record.
    """
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def process_to_parquet(input_path, output_path, drop_cols):
    """
    Read a .jsonl.gz file and write it to Parquet.

    Process:
        1. Opens the gzipped JSONL file and streams records line by line.
        2. Iterates records in batches of BATCH_SIZE.
        3. Drops unwanted columns from each batch.
        4. Infers the Parquet schema from the first batch, then appends
           subsequent batches to the same file using a single ParquetWriter.
        5. Closes the writer when all records are processed.

    The Parquet file uses Snappy compression, which gives a good balance of
    file size reduction and read/write speed.

    Parameters:
        input_path:  Path object pointing to the source .jsonl.gz file.
        output_path: Path object for the output .parquet file.
        drop_cols:   Set of column names to exclude from the output.
    """
    print(f"\nProcessing {input_path.name}...")

    if not input_path.exists():
        raise FileNotFoundError(
            f"{input_path} not found. Download it from "
            "https://amazon-reviews-2023.github.io/ and place it in data/raw/."
        )

    writer = None  # Initialised on first batch so schema can be inferred from data
    total = 0

    for batch in iter_batches(iter_jsonl_gz(input_path), BATCH_SIZE):
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
    Process all raw .jsonl.gz files and write them to Parquet.

    Execution order:
        1. books_reviews.parquet   -- full review text, largest file (~29.5M rows)
        2. books_metadata.parquet  -- book-level metadata (~4.4M rows)
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for source in SOURCES:
        process_to_parquet(
            input_path=RAW_DIR / source["input"],
            output_path=OUTPUT_DIR / source["output"],
            drop_cols=source["drop_cols"],
        )


if __name__ == "__main__":
    main()
