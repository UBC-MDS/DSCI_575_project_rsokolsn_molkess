# Amazon Book Query Assistant

## Project Description

This Query Assistant allows the user to search books from the Amazon Reviews 2023 Books category. With a simple UI, the user can select to search for books using either BM25 keyword search or semantic embedding search. The app then displays the top 5 books most relevant to the user's query.

### The Data

Due to the large amount of Amazon Books data, throughout this project we worked with a 10,000 book subset of the data, sampled in the `src/create_sample.py` script. This sample was then processed into LangChain documents using `src/document_processing.py`. Finally, these documents were transformed as necessary for information retrieval using the relevant `src/bm25.py` and `src/semantic.py` scripts. The sampled data and trained index files for both bm25 and semantic search can be found in `data/processed/sampled/`. This allows the user to simply run the application without having to run any of the data processing code themselves.

## Usage

### Set Up Environment Variables

Note as of Milestone 1 there are no environment variables necessary so you can skip to the next section

1. Copy `.env.sample` to `.env`
2. Fill in your own values for each variable.
3. `.env` is added to `.gitignore` so it is never committed to GitHub with secrets present.

### Running the App

1. Clone this respository and navigate to the directory in your terminal
2. If this is your first time exploring this project install the conda environment. In your terminal run:

```{bash}
conda create -f environment.yml
```

3. Activate the environment

```{bash}
conda activate amazon_books_assistant
```

4. Run the app locally

```{bash}
streamlit run app/app.py
```

### Run complete project from start to finish

1. Clone this respository and navigate to the directory in your terminal
2. If this is your first time exploring this project install the conda environment. In your terminal run:

```{bash}
conda create -f environment.yml
```

3. Activate the environment

```{bash}
conda activate amazon_books_assistant
```

4. Run the script to download the complete datasets (This can take up to several hours)

```{bash}
python src/load_data.py
```

5. Run the script to create the sample dataset

```{bash}
python src/create_sample.py
```

6. Run the script to create pickle file of LangChain documents

```{bash}
python src/document_processing.py
```

7. Run the script to create the BM25 retriever file.

```{bash}
python src/bm25.py
```

8. Run the script to create FAISS Index files for semantic search

```{bash}
python src/semantic.py
```

9. Run the app locally

```{bash}
streamlit run app/app.py
```

## Disclosure of Use of Generative AI Agents

This project made use of agentic coding tools (including Claude Code) during development. These tools were used for inline code suggestions and debugging assistance, particularly for optimizing the codebase to efficiently handle the large Parquet datasets. All AI-suggested code was reviewed, tested, and understood by the human authors before being incorporated into the project. The human authors take full responsibility for all code and content published in this repository, regardless of what tools were used during development.
