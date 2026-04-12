# Milestone 1: Qualitative Evaluation of Retrieval Methods

## 4.1 Create a Query Set

See `results/queries.csv` for our query set.

## 4.2 Retrieve results

Run `results/run_queries.py` to perform the searches. Results will be stored in `results/queries.csv`.

## 4.3 Compare Results

See `results/compare_results.ipynb` to view our interactive results analysis for five of our queries.

### `harry potter`

**BM25** correctly retrieves 5 books that specifically mention Harry Potter in the title.

**Semantic search** retrieves 3 books that specifically mention Harry Potter in the title, but also "Fanastic Beasts and Where to Find Them" which is part of the franchise but doesn't specifically mention Harry Potter in the title. It also retrieves "Kingdom of Carbonel", which is not part of the franchise.

**Better: BM25** since it finds 5 harry potter books, while semantic search only finds 4.

### `learn python programming beginner`

**BM25** places *Practical Programming: An Introduction to Computer Science Using Python 3.6* at rank 1, which is a very relevant result. The next book also mentions "basics", which indicates it is beginner friendly, though it is not as related to normal beginner python even though it has the word "python" in it. The third book is a "For Dummies" book which indicates beginner friendly, but I'm not sure what BeagleBone is and whether it is Python related. The last two are python related but not specifically beginner friendly (based on their titles).

**Semantic search** leads with *101 Extra Python Challenges* which is not beginner friendly but is Python related. Similarlyl, Python: Essential Reference is very related to Python but is likely a more advanced reference guide. The 3rd and 4th results are the same as the 2nd and 1st results from BM25, respectively. The last result, Think Stats, is not very related to the search query.

**Better: BM25** as it's top result is the best one. The top results for semantic search are very Python related, but not good beginner books.

### `overcoming grief after losing a loved one`

This is the clearest demonstration of semantic search's advantage in the query set.

**BM25** does return some grief related books (the 1st and 4th result are clearly grief related). I researched the second and third results and found that "Me For You" is a romantic fiction book with a main character who lost their spouse, so that is actually very relevant. I wasnt able to identify "Through It All" since there is no author. The last result seems to be the story of a missing person, so while it may be related to grief, I'm not sure it's necessarily about overcoming it after losing a loved one.

**Semantic search** gets all five results really spot on, returning several books very specifically about grieving after the loss of a loved one.

**Better: Semantic search** clearly does a better job of encoding the meaning of the search phrase and comes up with very relevant results.

### `self-help book for managing anxiety and stress at work`

Both methods perform reasonably well here because the query contains a good mix of specific terms ("anxiety," "stress") that are also semantically meaningful.

**BM25** top three recommendations seem very relevant to managing anxiety and stress based on their titles. However, rank 5, Loving Someone with OCD, is a bit off target since it appears to be more about personal relationships than managing at work. I also researched Emotional Core Therapy, the 4th recommendation, which is about stress but appears to be more centered on relationships rather than work specifically. Also note that The Undivided Self and Emotional Core Therapy both appear to maybe be more technical books, discussing scientific techniques, rather than more non-technical self-help style.

**Semantic search** picks the same top book and then Anxiety Antidotes in the second rank. It's suggestions for ranks 3 and 4 are also clearly related to managing your anxiety. The 5th rank book, Note to self, is more of a memoir about the author's struggle with depression and anxiety, so less of a good match since it is not a self-help book. Also note that the 4 top searches are very clearly self-help style books.

**Better: Semantic search** does a better job with the lower ranked matches, though there is a lot of overlap in the matches of both methods.

### `historical novel about World War 2 from a civilian perspective`

**BM25** fails almost entirely. Its rank 1 result, *Caves, Cannons and Crinolines*, is a Civil War novel, not about World War 2. It likely matched because of "historical," "novel," and "War" in its metadata. Rank 2, Just War Reconsidered, is an academic military ethics textbook. None of the five BM25 results are WWII historical fiction. It seems that BM25 captured historical novel from the search term but not World War 2. Interestingly, very few of the exact search terms appear in the titles of returned books, so it seems that BM25 is needing to go into the descriptions and reviews more to find relevant matches than in previous searches.

**Semantic search** correctly focuses on WWII across all five results. The first result, True Stories of World War II, seems like a very good match (I'm not sure if there are civilian perspectives inside, but it seems likely). The next four results are all about world war 2, but don't appear to be novels. It seems like semantic search captured the World War 2 portion of the query but not the historical novel piece.

**Better: Semantic search** gets the primary topic correct and has a promising first match. However, neither method handles multi-attribute constraints well. A hybrid approach with metadata filtering (e.g., filter to `category=fiction` before retrieval) might improve the results.

## 4.4 Summary of Insights

### Strengths and Weaknesses of Each Method

#### BM25

Strengths: 

- Strong at exact keyword and named entity matching (e.g., author names, titles, franchise names)
- Reliable when the user's vocabulary closely matches the document vocabulary

Weaknesses:

- Misses meaning when the query and document use different words for the same concept
- Common filler words ("novel," "best," "book") can skew scores and introduce false positives
- Struggles with multi-attribute constraint, can fulfill one or two aspects but not all

#### Semantic Search

Strengths:

- Captures intent and conceptual meaning without requiring keyword overlap
- Handles multi-keyword queries more holistically, with less sensitivity to irrelevant common words
- Better overall performance on queries where meaning matters more than exact terms

Weaknesses:

- Can miss verbatim matches and may not find a document that contains the exact query phrase
- Struggles with multi-attribute constraint, can fulfill one or two aspects but not all

### What Types of Queries Are Challenging for Both Methods?

Query 5 was difficult for both methods since it was asking for a lot at once (genre + specific topic + specific content): BM25 captured part of the query and semantic search captured a different part, but neither did well at capturing the entire thing. Neither appeared to capture the civilian perspective that the query was asking for. One thing we noticed is that sticker books appeared frequently in the results for both methods, indicating that neither was able to capture workbooks/activity books vs. books with text, which is not suprising.

### Where Would Advanced Methods Help?

- **Metadata filtering:** Pre-filtering by structured fields (genre category, fiction/non-fiction, age level, etc) before retrieval could seriously improve precision, especially on Queries 2 and 5.
- **Hybrid retrieval (BM25 + Semantic fusion):** Queries 1 and 2 did better with BM25 while 3 and 4 did better with semantic search, as expected. We could combine the two methods using  Reciprocal Rank Fusion to get the best of both worlds and do well on all four queries.
- **RAG:** For recommendation-style queries (e.g., "best sci-fi for someone who liked The Martian"), a language model could reason about what made a reference book distinctive and identify structurally similar books, going beyond surface embedding similarity.
