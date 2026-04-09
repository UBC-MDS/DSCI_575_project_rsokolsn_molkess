# Raw Data Download

To run this analysis you will need to download the raw data by running the `load_data.py` script. This script loads the data in batches from Huggingface datasets and saves it to `data/processed`.

1. Navigate to `src/load_data.py`.
2. Ensuring the amazon_books_assistant environment is active, run the script. This will download all necessary files and save them as parquet files in `data/processed`. This script takes approximately 1 hour to run, and will print out status updates in the terminal.

