# Amazon Book Query Assistant

## Project Description

This Query Assistant allows the user to search books from the Amazon Reviews 2023 Books category. With a simple UI, the user has the option of vanilla information retrieval via the Search Tab or using RAG to get a more conversational response. When using the search option, the user can select to search for books using either BM25 keyword search or semantic embedding search. The app then displays the top 5 books most relevant to the user's query. Using the RAG option, an LLM uses the returned items from a Hybrid search and provides an explanation for which books are most relevant to the user's query. Explanation of LLM choice can be found in `milestone2_discussion.md`

![Hybrid RAG Diagram](img/RAG%20diagram.png)

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

The `average_rating`, `parent_asin` (unique ID), `features` (named blurb), and `title` will be stored as metadata for each document.

### Search Algorithms

#### BM25

BM25 (Best Match 25) is a keyword-based algorithm which scores documents by how well they match a given query. Given a query, BM25 scores all documents in the index and returns the top matches ranked by relevance. It is fast, interpretable, and works well for exact keyword matches, but does not capture semantic meaning. This is becuase it uses a sparse vector representation of each document and query.

#### FAISS

Semantic search algorithms like FAISS use dense vector embeddings to find documents that are conceptually similar to a query, even when they share no keywords in common. Each document is converted into a high-dimensional vector using a pretrained language model, capturing its meaning rather than just its words. These vectors are stored in an index and are compared against a dense vector embedding of a given query. The algorithm uses euclidean distance to measure the similarity between vectors and returns the documents that are most similar to the query.

## Set Up

### Set Up Environment Variables

For Milestone 2 and the final submission, you must add your Groq API key in order to use LLM search in the web app. To do so, follow the instructions below.

#### Generate the key

1. Navigate to [](https://console.groq.com/keys) and sign in or set up an account.
2. Click "Create API Key". Name the key and set the expiration to whatever you want. Copy the key.

#### Add the key to the `.env` file

1. Copy `.env.example` to `.env`.
2. Inside `.env`, replace "your-groq-api-key" with your copied key, wrapped in double quotes, and save the file.

Note: `.env` is added to `.gitignore` so it is never committed to GitHub with secrets present.

### Running the App

1. Clone this respository and navigate to the directory in your terminal
2. If this is your first time exploring this project install the conda environment. In your terminal run:

```{bash}
conda env create -f conda_environment.yml
```

3. Activate the environment

```{bash}
conda activate amazon_books_assistant
```

4. Run the app locally

```{bash}
streamlit run app/app.py
```

### RAG

We implemented two RAG pipelines. One using a semantic retriever and the other using a custom built hybrid retriever. To use the semantic pipeline:

1. Follow the instructions above to set up the conda environment and set up your Groq API key.
2. Enter your query on line 24 of the `rag_pipeline.py` script. Save the script.
3. In your terminal navigate to the repository directory and run:

```{bash}
python src/rag_pipeline.py
```

The Hybrid RAG pipeline which uses a custom built hybrid retriver with a reciprocal rank function combining the keyword and semantic searches can most easily be used via the web app.

### Run complete project from start to finish

Note: You do not need to run the complete project in order to use the app. Completing this workflow will likely take several hours due to the size of the full dataset. The pickle file of LangChain documents, the BM25 retriever file, and the FAISS index file of the 10,000 book sample are all stored in the Github repository and are downloaded when you cloned the repo. You can run the app and explore the interactive analyses in `results/compare_results.ipynb` using these files. To run the EDA in `notebooks/milestone1_exploration.ipynb`, you will need to download the full dataset.

1. Clone this respository and navigate to the directory in your terminal
2. If this is your first time exploring this project install the conda environment. In your terminal run:

```{bash}
conda create -f conda_environment.yml
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

## Usage Examples

### Web App

Once the app is running, navigate to `http://localhost:8501` in your browser.

**Search Tab — BM25 keyword search:**

```text
Query: "mystery novels set in Victorian England"
Method: BM25 Keyword
```

**Search Tab — Semantic search:**

```text
Query: "books about grief and healing after loss"
Method: FAISS Semantic
```

Both search methods return the top 5 results. Each result shows the title, author, average rating, retrieval score, and a short description of the book.

**RAG Tab — LLM-powered recommendation:**

```text
Query: "What should I get for my 6th grade niece who loves dinosaurs?"
```

The RAG tab uses the hybrid retriever (BM25 + semantic) and returns an LLM-generated explanation alongside the source books.

### Programmatic Usage

You can call the retrieval functions directly from Python:

```python
from src.bm25 import bm25_search
from src.semantic import semantic_search

# BM25 keyword search — returns list of dicts
results = bm25_search("mystery novels set in Victorian England", k=5)

# Semantic search — returns list of dicts
results = semantic_search("books about grief and healing", k=5)

# Each result has the shape:
# {"title": ..., "author": ..., "rating": ..., "blurb": ..., "score": ...}
```

## Description of New Features

Below is a description of new features added in each version.

### v0.1.0

- load the books data from HuggingFace by running `load_data.py`
- create a 10,000 book sample of the data by running `create_sample.py`
- process the reviews and metadata into LangChain format by running `document_processing.py`
- create the semantic search index by running `semantic.py`
- create the BM25 retriever by running `bm25.py`
- explore the dataset in `milestone1_exploration.ipynb` 
- see a comparison of BM25 and Semantic search results on 5 example queries in `compare_results.ipynb` and `milestone1_discussion.md`
- run the web app locally to perform any BM25 or Semantic searching that you want and see the top 5 results visually

### v0.2.0

- get LLM generated search results under the "RAG" tab in the web app
- see the RAG pipeline in action in `rag_pipeline.py`
- use hybrid (BM25 + Semantic) search results with the `hybrid_retriever()` function from `hybrid.py`
- explore `milestone2_rag.ipynb` to see the LLMs response on 10 example queries
- read `milestone2_discussion.md` to learn more about the model choice, prompt engineering decisions, and RAG evaluation on example queries

### v0.3.0

- access the web app publically at <http://amazonbooks.streamlit.app>
- see the comparison between llama-3.1-8b-instant LLM, which is implemented in the web app, with _____ (add name) LLM in _____ (add file here)

Note: Streamlit's free tier has limited memory and our app requires loading the BM25 and Semantic indices into memory alongside the memory required for the actual computations. This means that after 5ish queries the deployed app runs out of memory. Streamlit displays a warning that the free tier memory has run out and offers some options. To reset the memory and continue using the app, select the option to 'Reboot'. There will be a warning that this impacts all users, which is ok. Then, refresh the webpage to see the app running as expected.

## Disclosure of Use of Generative AI Agents

This project made use of agentic coding tools (including Claude Code) during development. These tools were used for inline code suggestions and debugging assistance, particularly for optimizing the codebase to efficiently handle the large Parquet datasets. All AI-suggested code was reviewed, tested, and understood by the human authors before being incorporated into the project. The human authors take full responsibility for all code and content published in this repository, regardless of what tools were used during development.
