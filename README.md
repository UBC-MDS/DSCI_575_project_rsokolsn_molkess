# Amazon Book Query Assistant

## Project Description

This Query Assistant allows the user to search books from the Amazon Reviews 2023 Books category. With a simple UI, the user can select to search for books using either BM25 keyword search or semantic embedding search. The app then displays the top 5 books most relevant to the user's query.

### The Data

Due to the large amount of Amazon Books data, throughout this project we worked with a 10,000 book subset of the data, sampled in the `src/create_sample.py` script. This sample was then processed into LangChain documents using `src/document_processing.py`. Finally, these documents were transformed as necessary for information retrieval using the relevant `src/bm25.py` and `src/semantic.py` scripts. The sampled data and trained index files for both bm25 and semantic search can be found in `data/processed/sampled/`. This allows the user to simply run the application without having to run any of the data processing code themselves.

### Data Preproccesing

For both BM25 and FAISS semantic searches we chose to build LangChain documents with a single document content string which is concatenated from the following fields: 

- `metadata.title`
- `metadata.subtitle`
- `metadata.author`
- `metadata.description` (joined if list)
- `metadata.features` (joined if list)
- `metadata.categories` (joined if list)
- Aggregated `reviews.title` and `reviews.text` (concatenation of reviews per book)

This concatenated string was then tokenized for BM25 and embedded for semantic search. Additionally, for BM25 keyword search, we additionally converted all of the content strings to lower case, removed any punctuation, and removed common words using the `nltk` stopwords corpus. 

The `average_rating` and `parent_asin` (unique ID) will be stored as metadata for each document.

### Search Algorithms

#### BM25

BM25 (Best Match 25) is a keyword-based algorithm which scores documents by how well they match a given query. Given a query, BM25 scores all documents in the index and returns the top matches ranked by relevance. It is fast, interpretable, and works well for exact keyword matches, but does not capture semantic meaning. This is becuase it uses a sparse vector representation of each document and query.

#### FAISS

Semantic search algorithms like FAISS use dense vector embeddings to find documents that are conceptually similar to a query, even when they share no keywords in common. Each document is converted into a high-dimensional vector using a pretrained language model, capturing its meaning rather than just its words. These vectors are stored in an index and are compared against a dense vector embedding of a given query. The algorithm uses euclidean distance to measure the similarity between vectors and returns the documents that are most similar to the query.

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

Note: You do not need to run the complete project in order to use the app. Completing this workflow will likely take several hours due to the size of the full dataset. The pickle file of LangChain documents, the BM25 retriever file, and the FAISS index file of the 10,000 book sample are all stored in the Github repository and are downloaded when you cloned the repo. You can run the app and explore the interactive analyses in `results/compare_results.ipynb` using these files. To run the EDA in `notebooks/milestone1_exploration.ipynb`, you will need to download the full dataset.

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
