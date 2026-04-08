# Raw Data Download

To run this analysis you will need to download the raw data. You can either navigate to [](https://amazon-reviews-2023.github.io/) and download the 'Books' review and meta data, or download the data in batches from Huggingface datasets by running the `load_data.py` file.

## Downloading Data from [](https://amazon-reviews-2023.github.io/)

Navigate to [](https://amazon-reviews-2023.github.io/) and download the 'Books' review and meta data

Save the files to this folder in your local environment but do not push them to GitHub. (This should be prevented by the `.gitignore`)

- `Books.jsonl.gz`
- `meta_Books.jsonl.gz`

After downloading the data, navigate to `process_raw_data.py`. Ensuring the amazon_books_assistant environment is active, run the script. This will process the raw files and save them as parquet files in `data/processed`.

**note: add how to manually download splits?**

## Downloading Data using `load_data.py`

Navigate to `src/load_data.py`. Ensuring the amazon_books_assistant environment is active, run the script. This will download all necessary files and save them as parquet files in `data/processed`. This script takes approximately 1 hour to run, and will print out status updates in the terminal.
