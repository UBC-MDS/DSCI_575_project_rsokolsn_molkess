# Final Discussion

## Step 1: Improve Your Workflow

### Dataset Scaling
As our pipeline already used a sample of 10,000 products (books), we did not implement any additional changes to our sampling strategy.

### LLM Experiment

### Models
For this experiment, we compared the Llama 3.1 8B (llama-3.1-8b-instant) model with the GPT OSS 20B (openai/gpt-oss-20b) model. The Llama model has a speed of 560 T/sec, a context window of 131,072 toeksn, and 131,072 max completion tokens. The GPT model has a speed of 1000 T/sec, a context window of 131,072 tokens, and 65,536 max completion tokens. We wanted to compare with this model since it is larger (20B vs. 8B) and is from a different company (OpenAI vs. Meta), so we expect it to have significantly different capabilities.

### Results

#### Query: stephen king horror novel

=== llama-3.1-8b-instant ===

Based on the provided Amazon dataset, I recommend the following Stephen King horror novels:

1. **Thinner** (4.5/5) - A #1 national bestseller about a man's quest to reverse his nightmare and find the source of his weight loss.
2. **The Green Mile** (4.8/5) - A character-driven story about a death row supervisor who discovers one of the prisoners may have supernatural healing powers.
3. **FAIRY TALE** (4.4/5) is actually a non-horror book by Stephen King, but I'll exclude it from the list.

These novels are all highly rated and classified as horror by Amazon, making them great recommendations for fans of the genre.

=== openai/gpt-oss-20b ===

**Recommended Stephen King horror novel:**  
**Thinner** – A chilling tale of a man cursed to lose weight at an alarming rate, blending psychological dread with supernatural revenge. The story is widely recognized as one of King’s classic horror works.

#### Query: romance novel with enemies to lovers trope

=== llama-3.1-8b-instant ===

Based on the Amazon dataset, I recommend the following romance novels with the enemies-to-lovers trope:

1. **Reign Returned: The Felserpent Chronicles** by Katie Keridan - This young adult fantasy romance novel features a complex story with a great romance that brings people together, but ultimately tears them apart. The enemies-to-lovers trope is a significant part of the story, making it a great fit for your request.

2. **Letting Love Win** by Alysia S. Knight - While the description doesn't explicitly mention the enemies-to-lovers trope, the rating and good reviews suggest that it might be a romance novel with a strong focus on relationships, potentially including this trope.

Please note that the description for **Letting Love Win** is quite brief, so it's difficult to make a definitive recommendation. However, based on the available information, it's worth considering.

Unfortunately, I don't have enough information to recommend books from the **For a Glance (Serpent's Throne Trilogy)** and **Something So Right: Something So, Book 1** series as they don't fit the enemies-to-lovers trope explicitly mentioned in the context.

=== openai/gpt-oss-20b ===

**Recommendation**

- **Reign Returned: The Felserpent Chronicles** – The story follows Kyra, an Astral healer, and Sebastian, a Daeval assassin from rival realms. Their initial alliance is forced and hostile, but as they work together they develop a deep romance, fitting the enemies‑to‑lovers trope.

#### Query: a story about a young person finding their identity

=== llama-3.1-8b-instant ===

Based on the context provided, here are some book recommendations that tell a story about a young person finding their identity:

1. **That Guy in Our Women's Studies Class** by Allan D. Hunter: This non-fiction memoir shares the story of a genderqueer individual, Derek, who navigates the complexities of identity and intersectionality in a women's studies class.
2. **Camp** by Lev AC Rosen: This novel follows 16-year-old Randy, who reinvents himself as "Del" to fit into a summer camp for queer teens, exploring the tension between self-acceptance and conformity.
3. **Holding the Light; A Soldier's Journey** by Abbie Combs: Although the blurb doesn't explicitly mention identity, this picture book shares a true story of a young person finding their purpose and overcoming challenges, which can be a powerful metaphor for self-discovery.

These books offer relatable and thought-provoking stories about identity, self-discovery, and growth, which may resonate with young readers and adults alike.

=== openai/gpt-oss-20b ===

**Books that explore a young person discovering their identity**

| Title | Why it fits |
|-------|-------------|
| **That Guy in Our Women’s Studies Class** by Allan D. Hunter | A memoir‑style narrative of a gender‑queer male navigating women’s studies, race, and class. It follows Derek’s journey of self‑acceptance and the complex ways identity is formed. |
| **Camp** by Lev AC Rosen | A YA novel set at a queer camp where the protagonist Randy redefines himself, confronts toxic masculinity, and learns what true self‑love looks like. |

Both books offer relatable, coming‑of‑age stories where the protagonists grapple with and ultimately embrace their identities.

#### Query: mystery thriller with unreliable narrator set in small town

=== llama-3.1-8b-instant ===

Based on the Amazon dataset, I recommend the following books that fit your criteria:

1. **Guilty by Association** by Brad Cooper: This psychological thriller is set in a small town, and its fast-paced plot and unexpected twists make it a great fit for a mystery thriller with an unreliable narrator. (Rating: 4.2)
2. **A Legacy of Lies: A Rock Ridge Mystery**: Although not explicitly stated as an unreliable narrator, the book's complex characters and layered story make it a great fit for fans of mystery thrillers set in small towns. (Rating: 4.3)
3. **Witch & Famous (A Westwick Witches Cozy Mystery)**: This cozy mystery series has a small-town setting and features a cast of complex characters, including witches with their own secrets and motivations. While not necessarily an unreliable narrator, the book's blend of mystery and humor makes it a great fit for fans of the genre. (Rating: 3.9)

These recommendations are based on the provided Amazon dataset and may not be exhaustive, but they should provide a good starting point for finding a mystery thriller with an unreliable narrator set in a small town.

=== openai/gpt-oss-20b ===

I’m sorry, but the data I have doesn’t include any titles that specifically match a mystery‑thriller with an unreliable narrator set in a small town.

#### Query: best science fiction book for someone who liked The Martian

=== llama-3.1-8b-instant ===

Based on the Amazon dataset, I recommend:

1. **Old Man's War** by John Scalzi: This book is a New York Times bestselling science fiction novel that explores themes of space travel, intergalactic politics, and humanity's place in the universe. It has a similar sense of adventure and scope to The Martian, and is the first book in a popular series.

2. **REVOLT OF THE GALAXY** by Stephen Goldin: This book is the 10th installment in the Family d'Alembert series, which features epic space battles, intergalactic politics, and a sense of adventure reminiscent of The Martian. While it's part of a larger series, it can be read as a standalone novel.

3. **Transit to Scorpio** by Alan Burt Akers: This book is a science fiction adventure that follows the story of Dray Prescot and his wife, as they explore the galaxy and face various challenges. It has a similar sense of space travel and exploration to The Martian, and is part of a popular series.

All three of these books have received high ratings on Amazon and are recommended for fans of science fiction and adventure stories.

=== openai/gpt-oss-20b ===

**Recommendation based on the Amazon dataset**

**Old Man’s War Boxed Set – John Scalzi**  
- *Why it fits:* This collection delivers a fast‑paced, realistic space‑opera adventure that blends survival, human ingenuity, and the challenges of a new frontier—much like the survival‑driven, scientifically grounded tone of *The Martian*.  

**Revolt of the Galaxy – Stephen Goldin**  
- *Why it fits:* Another high‑energy space‑adventure that explores planetary colonization, military strategy, and the human spirit in a hostile galaxy, echoing the lone‑survivor vibe of *The Martian*.

Both titles are solid science‑fiction choices that match the excitement and scientific curiosity of *The Martian*.

#### Key Observations

- both models favor a format with an intro sentence indicating these are recommended based on the amazon dataset, then some kind of list/bullet point format to display the recommended book titles along with a sentence about the book and/or why it matches the query, then a summary sentence.
- the Llama model starts all of it's replies with "Based on the", e.g. "Based on the Amazon dataset, I recommend..." or "ased on the context provided, here are some book recommendations..." while the GPT model has more diverse starting sentences and often favors more of a shorter, title-esque format with bold letters, rather than a sentence.
- the Llama model always lists the recommended books in an ordered list (i.e. 1, 2, 3), while the GPT model lists the books differently in every answer
- the GPT model indicated it had no matching books for the query "mystery thriller with unreliable narrator set in small town", whereas the Llama model recommended three books, despite indicating that the books may not match all of the criteria of the search (i.e. two of the books it indicated they may not have an unreliable narrator).
- similarly, for the "romance novel with enemies to lovers trope", both models returned the same best top match, but the Llama model tried to recommend a second book, even though it noted it it's description that it doesn't mention enemies to lovers, whereas the GPT model only recommended the one good match
- in general, the Llama model recommends more books that the GPT model
- the top recommendations are always identical for the two models
- the GPT model tries to put lots of formatting (e.g. bolding, italics putting in markdown tables, etc) into it's answers, while the Llama model only does ordered lists and emphasizing the book titles.
- for the "best science fiction book for someone who liked The Martian" query, both models do a good job referencing why they chose the books they are recommending specifically in relation to The Martian, but the GPT model is more specific, for example GPT references the "the lone‑survivor vibe of *The Martian*" whereas Llama mentions the more generic "similar sense of space travel and exploration to The Martian".

#### Discussion

Overall, it seems that both models agree on the top match from the context (the 5 books provided by hybrid rag search), but the GPT model does a better job of being more concise and only recommending good matches, whereas the Llama model will put the good match first but then continue to recommend more books, even when it notes that they may not include everything the prompt asked for. That being said, the Llama model is much more consistent in it's formatting than GPT. This is likely due to the open nature of the system prompt and the Llama model being smaller and less diverse than the GPT model, so it still returns a consistent format even when that is not explicitly asked for. I hypothesize that GPT would perform consistenly if provided a prompt with more specific guidelines on formatting.

#### Model Selection

These results indicate the switching to the openai/gpt-oss-20b model would provide more concise and relevant results for our users. That being said, we have elected not to switch at this time. Our original reasoning for choosing the Llama model was that it is lightweight and runs quick enough for our purposes, and it has one of the highest rate limits through Groq's free access tier. These reasons are still very relevant to our model selection decision making. Since both models consistently returned the same top 1-2 recommendations, we believe that we can still provide the highest quality recommendations to users without switching the larger and more expensive/free-tier limited GPT model. That being said, we would recommend additional prompt engineering to try to improve the ability of the Llama model to only make good match recommendations and to make no recommendations if there are no good matches.

## Step 2: Additional Feature (state which option you chose)

### Basic App Deployment

We chose to deploy our app using Streamlit Cloud. This required several steps. First of all, I made our repository public. While Streamlit has the ability to resolve dependencies and set up an environment using a conda `environment.yml` file, this is very slow. To speed up the process, I created a pip `requirements.txt` file which streamlit is more quickly able to handle. This took some troubleshooting to ensure package version compatibility but was successful. Our deployed app can be found at  <http://amazonbooks.streamlit.app>. 

One thing to note is that Streamlit's free tier has limited memory and our app requires loading the BM25 and Semantic indices into memory alongside the memory required for the actual computations. This means that after 5ish queries the deployed app runs out of memory. Streamlit displays a warning that the free tier memory has run out and offers some options. To reset the memory and continue using the app, select the option to 'Reboot'. There will be a warning that this impacts all users, which is ok. Then, refresh the webpage to see the app running as expected. 
  
## Step 3: Improve Documentation and Code Quality

### Documentation Update

To improve the README, we added two sections of usage examples which give example usage instructions for the different kinds of searches using the web app or programmatically, as well as a section for description of new features which describes the features added in each version (i.e. Milestone). We also updated the Set Up instructions to be more clearly formatted and fixed a few typos in the instructions.

### Code Quality Changes

To improve the code quality of the repository, we ensured that every function is properly documented with at least one line of docstring, and that every script (i.e. `.py` file) is documented with a summary of the contents of the script at the top of the file. We created a `config.py` file that contains constants and paths used across the codebase and removed any hardcoded file paths. We have also ensured that no API keys were present in the source code by using a `.env` file, and double checked that the environment files are up to date (note that we have two environment files: see Basic App Deployment for more information) and that there are no temporary files or large artifacts in Github. Lastly, we ensured that the large data files and the secret `.env` file are not accidentally uploaded to Github by updating the `.gitignore` to include these files.

## Step 4: Cloud Deployment Plan

Though we did choose to deploy our web app suing Streamlit Cloud, a more robust and stable deployment would involve some substantial architecture changes. Since we have most recently worked in the AWS infrastructure, we will outline a deployment plan using those tools.

We currently took a sample of the complete dataset and store the processed sample in a pickle file in GitHub alongside the BM25 retriever and Semantic index. To increase storage capacity, we would set up the initial data download pipeline to put the raw data directly into and S3 bucket. Since we already use a partitioned parquet file, this would be a fairly straightforward change. We would also store the processed data, BM25 retriever and Semantic index in the same bucket in a separate folder.

To ensure all data stays up to date, we would use Lambda functions set to run on a nightly schedule. First, the function would download any new data saving it in the `raw` folder of the S3 bucket. Then, the function would do the data processing to store the products as LangChain documents and rebuild the indices. We would refactor as much of these computations as possible to use DuckDB so that it can work with a larger portion of the dataset. 

We currently are hosting the web app using Streamlit Cloud free tier. While this is lightweight and works for now, we are already running into some memory issues as outlined above. For a cost effective way to scale the app, we could leverage the AWS App Runner, which autoscales to handle concurrent users. This would take some work as we would also need to set up a Docker container and image for the app. However, in the case of a fully deployed app, this extra effort would be worth it for the cost-savings and effiency. 

We currently handle the LLM Inference via API using the Groq API and this could be easily moved into the AWS infrastructure outlined above. By using an API, DuckDB lazy loading and the AWS App Runner, it would be fairly straightforward to fully cloud deploy our project.
