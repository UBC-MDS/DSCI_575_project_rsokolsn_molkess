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
(See Step 4 above for required subsections)