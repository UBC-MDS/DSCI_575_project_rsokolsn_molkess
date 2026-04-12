# Milestone 1: Qualitative Evaluation of Retrieval Methods

## 4.1 Create a Query Set

See `results/queries.csv` for our query set.

## 4.2 Retrieve results

Run `results/run_queries.py` to perform the searches. Results will be stored in `results/queries.csv`.

## 4.3 Compare Results

See `results/compare_results.ipynb` to view our interactive results analysis for five of our queries.

### `harry potter`

**BM25** correctly retrieves 5 books that specifically mention Harry Potter in the title.

**Semantic search** retrieves 2 books that specifically mention Harry Potter in the title, but also "Fanastic Beasts and Where to Find Them" which is part of the franchise but doesn't specifically mention Harry Potter in the title. "Wizard's Hall" is apparently a different book that came out before Harry Potter and is very similar, so we can see the semantic search finding similar titles here. The Riddle of the New Testament does not seem related though.

**Better: BM25** does better since it retrieves 5 related books, while semantic search only retrieves 3.

### `learn python programming beginner`

**BM25** finds 3 books that are specifically Python related, though only the first result seems beginner friendly. The last two results seem to be beginner programming related, but no Python related.

**Semantic search** leads with 101 Extra Python Challenges which is not beginner friendly but is Python related. After that is the same as the first result from BM25. The third result is python related but doesn't seem beginner friendly, and the fourth is beginner friendly but it's unclear whether it is specifically Python related. The fifth is related to coding but is for Scratch, not Python, and does not appear beginner friendly.

**Better: BM25** as it's top result is the closest match to the search query. Both algorithms struggled a lot with matching the "beginner" part of the query.

### `overcoming grief after losing a loved one`

**BM25** does return some grief related books (the 2nd and 4th are clearly grief related) but mostly the results seem unrelated. Interestingly, the 4th result appears the most related based on the title, yet it is only the 4th ranked. (Looking at semantic search, we can see that the same result is ranked 2nd.)

**Semantic search** gets all five results really spot on, returning several books very specifically about grieving after the loss of a loved one such as a child or partner.

**Better: Semantic search** clearly does a better job of encoding the meaning of the search phrase and comes up with very relevant results.

### `self-help book for managing anxiety and stress at work`

**BM25** top two recommendations seem very relevant to managing anxiety and stress based on their titles. I researched Emotional Core Therapy, the 3rd recommendation, which is about stress but appears to be more centered on relationships rather than work specifically. Loving Someone with OCD is not really a self-help book or about stress at work, and the complete credit repair kit is very off the mark. The last result is a coloring book for stress relief, which is related to the "stress" keyword but not much else in the query.

**Semantic search** picks the same top book, but it's recommendations for the 2nd and 3rd rank are much more relevant and clearly self-help style books. The 4th and 5th ranked books are less about stress and anxiety in the workplace, but are self-help type books about mental health in general. The 5th ranked book is the same as the 2nd ranked book in BM25.

**Better: Semantic search** does a better job, producing 3 good top matches while BM25 only produces one good top match.

### `historical novel about World War 2 from a civilian perspective`

**BM25** fails entirely at capturing the World War 2 piece of the query. Its rank 1 result, *Caves, Cannons and Crinolines*, is a Civil War novel, not about World War 2. It likely matched because of "historical," "novel," and "War" in its metadata. Rank 2, Just War Reconsidered, is an academic military ethics textbook. None of the five BM25 results are about world war 2, though they do mostly appear to be historical novels about war. It seems that BM25 captured "historical novel" and "war" from the search term but not World War 2 specifically. Interestingly, very few of the exact search terms appear in the titles of returned books (besides "war"), so it seems that BM25 is needing to go into the descriptions and reviews more to find relevant matches than in previous searches.

**Semantic search** correctly focuses on WWII across all five results but it seems to be pulling mostly academic books rather than novels. The 5th result, Raj and Norah, is a novel and is "a true story of love lost and found in WWII", which appears to actually be a very good match to the query, so it's odd that it is only in 5th place.

**Better: Neither** algorithm gets a very good match. Semantic search manages to capture World War 2 in all of it's results, but not historical novel. BM25 seems to capture the historical novel part of the query and that they are looking for a war theme, but does not return any results about World War 2 in particular. Neither method appears to have captured the "civilian perspective" piece of the search query.

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
