# Amazon Book Query Assistant

## Project Description

This Query Assistant allows the user to search books from the Amazon Reviews 2023 Books category. Due to the large amount of data throughout this project we worked with a 20,000 book subset of the data, sampled in the `src/create_sample.py` script.

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


## Disclosure of Use of Generative AI Agents

This project made use of agentic coding tools (including Claude Code) during development. These tools were used for inline code suggestions and debugging assistance, particularly for optimizing the codebase to efficiently handle the large Parquet datasets. All AI-suggested code was reviewed, tested, and understood by the human authors before being incorporated into the project. The human authors take full responsibility for all code and content published in this repository, regardless of what tools were used during development.
