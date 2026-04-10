# Amazon Book Query Assistant

## Project Description

This Query Assistant allows the user to search books from the Amazon Reviews 2023 Books category. Due to the large amount of data throughout this project we worked with a 20,000 book subset of the data, sampled in the `src/create_sample.py` script.

## Usage

### Environment Set Up

1. Copy `.env.sample` to `.env`
2. Fill in your own values for each variable.
3. `.env` is added to `.gitignore` so it is never committed to GitHub with secrets present.

## Disclosure of Use of Generative AI Agents

This project made use of agentic coding tools (including Claude Code) during development. These tools were used for inline code suggestions and debugging assistance, particularly for optimizing the codebase to efficiently handle the large Parquet datasets. All AI-suggested code was reviewed, tested, and understood by the human authors before being incorporated into the project. The human authors take full responsibility for all code and content published in this repository, regardless of what tools were used during development.
