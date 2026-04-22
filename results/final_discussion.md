# Final Discussion

## Step 1: Improve Your Workflow

### Dataset Scaling
- Number of products used
- Changes to sampling strategy (if any)

### LLM Experiment
- Models compared (name, family, size)
- Results and discussions
    - Prompt used (copy it here)
    - Results
- Which model you chose and why

## Step 2: Additional Feature (state which option you chose)

### Basic App Deployment

We chose to deploy our app using Streamlit Cloud. This required several steps. First of all, I made our repository public. While Streamlit has the ability to resolve dependencies and set up an environment using a conda `environment.yml` file, this is very slow. To speed up the process, I created a pip `requirements.txt` file which streamlit is more quickly able to handle. This took some troubleshooting to ensure package version compatibility but was successful. Our deployed app can be found at  <http://amazonbooks.streamlit.app>. 

One thing to note is that Streamlit's free tier has limited memory and our app requires loading the BM25 and Semantic indices into memory alongside the memory required for the actual computations. This means that after 5ish queries the deployed app runs out of memory. Streamlit displays a warning that the free tier memory has run out and offers some options. To reset the memory and continue using the app, select the option to 'Reboot'. There will be a warning that this impacts all users, which is ok. Then, refresh the webpage to see the app running as expected. 
  
## Step 3: Improve Documentation and Code Quality

### Documentation Update
- Summary of `README` improvements

### Code Quality Changes
- Summary of cleanups

## Step 4: Cloud Deployment Plan

Though we did choose to deploy our web app suing Streamlit Cloud, a more robust and stable deployment would involve some substantial architecture changes. Since we have most recently worked in the AWS infrastructure, we will outline a deployment plan using those tools.

We currently took a sample of the complete dataset and store the processed sample in a pickle file in GitHub alongside the BM25 retriever and Semantic index. To increase storage capacity, we would set up the initial data download pipeline to put the raw data directly into and S3 bucket. Since we already use a partitioned parquet file, this would be a fairly straightforward change. We would also store the processed data, BM25 retriever and Semantic index in the same bucket in a separate folder.

To ensure all data stays up to date, we would use Lambda functions set to run on a nightly schedule. First, the function would download any new data saving it in the `raw` folder of the S3 bucket. Then, the function would do the data processing to store the products as LangChain documents and rebuild the indices. We would refactor as much of these computations as possible to use DuckDB so that it can work with a larger portion of the dataset. 

We currently are hosting the web app using Streamlit Cloud free tier. While this is lightweight and works for now, we are already running into some memory issues as outlined above. For a cost effective way to scale the app, we could leverage the AWS App Runner, which autoscales to handle concurrent users. This would take some work as we would also need to set up a Docker container and image for the app. However, in the case of a fully deployed app, this extra effort would be worth it for the cost-savings and effiency. 

We currently handle the LLM Inference via API using the Groq API and this could be easily moved into the AWS infrastructure outlined above. By using an API, DuckDB lazy loading and the AWS App Runner, it would be fairly straightforward to fully cloud deploy our project.
