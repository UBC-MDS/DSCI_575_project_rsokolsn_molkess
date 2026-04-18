# Milestone 2: RAG Pipeline Discussion

## Model Choice

We chose to use the Llama 3.1 model with 8 billion parameters through Groq. We chose this model because it is quite lightweight and while having enough computing power to run quickly for our purposes. Additionally, it is one of the models with the highest rate limits using Groq's free tier of access.

## System Prompt Variants

We tried three system prompt variants, documented in `prompts.py`. The first prompt is the longest, which asks the LLM for 1 - 2 book recommendations in 1-3 sentences and encourages it to justify it's answer and quote items from the documents. The second prompt has the same guidelines about only using the context and not making up an answer, but does not mention or encourage the LLM to reference book titles or provide justification. THe third does not specify the number of books to write or the response length, just to be concise and reference book titles and provide a brief justification.

In the first prompt we specified 1-3 sentence responses. The LLM always returned a 3 sentence response, and the sentences were extremely long and run-on, to the point where each sentence was it's own short paragraph. That being said, the content returned was very good and referenced incredibly specific details from the reviews.

The second prompt returned results very similar to the first, and justified it's answers with the same level of detail, despite the prompt not asking for that explicitly. Additionally, the second prompt more frequently directly quoted the documents (e.g the description and reviews), even though we didn't ask for that in the second prompt but we did in the first (and it rarely did). It seems that less detail actually caused the second prompt to behave closer to how we wanted. Like the first prompt, the second prompt uses long run-on sentences to stay within the 3 sentence limit.

The third prompt was the most open-ended and did not specify how many books to recommend or what length of response to give. Interestingly, it had the most concise responses, sometimes with only two sentences (one per book), whereas the other two responses always went up to 3 sentences or over.

It seems that specifying a desired response length and number of books to return didn't really do much to actually constrain the LLM. Additionally, it always returned at the upper limit of the range (3 sentences and 2 books).

Overall, with all three prompts, the LLM did not just return the top hybrid retriever results. When the prompt had complicated context, e.g. a particular age range, it found more relevant results than the top result(s). All three prompts did a good job of staying within the context and providing brief explanations. Additionally, when given an extremely specific query, all three prompts correctly indicated that they could not find an exact match in the dataset, and did not try to recommend something outside of the provided context. That being said, they did then still try to recommend two books from the context, indicating that none of the prompts were clear enough that the LLM is encouraged not to recommend any books if it cannot find a good match.

Overall, we chose the third  prompt. It seems that the LLM's default response length, amount of detail, and number of recommendations corresponds with what we want from it. We found that having fewer constraints generated more useful responses with an appropriate amount of detail. In general, when the LLM made a simple recommendation (usually that matched up with the top 2 results from hybrid search), it only wrote one medium length sentence per book. When the model chose books that were not the top choices of the hybrid retriever it usually justified them a bit more, which is the desired behaviour. While it never made up any books not in the context, the LLM does still have a hard time with indicating that there is no appropriate match and not making a recommendation. While it will often correctly indicate no appropriate match somewhere in the response, it still always makes two recommendations, and sometimes the indication is in the middle of the text, so the user may not see it.

## RAG Evaluation

You can see a complete overview of the results for each of our ten queries in `notebooks/milestone2_rag.ipynb`

### `harry potter`

```
Based on the provided context, here are some book recommendations related to Harry Potter:

1. **Harry Potter Film Wizardry (Arabic Edition)** by Brian Sibley: This book is a great choice for fans who want to explore the behind-the-scenes magic of the Harry Potter films.
2. **Harry Potter: The Dark Arts (Tiny Book)** by Insight Editions: This collectible art book features facts and art from the Harry Potter films, and is a great addition to any fan's collection.
3. **Complete 1-st Edition Harry Potter Full Book Set Volumes 1-7 Hardback** by J.K. Rowling: If you're looking to collect the entire series, this hardback set is a great option.
4. **Harry Potter y el legado maldito / Harry Potter and the Cursed Child (Spanish Edition)** by J.K. Rowling: This play script is a great addition to any fan's collection, and explores the story of Harry's son Albus.
5. **Fantastic Beasts and Where to Find Them** by J.K. Rowling: This companion book to the Harry Potter series explores the magical creatures of the wizarding world.
```

This was a query where both the BM25 and Semantic Searches performed well on their own. Given this, we found that the hybrid retriever and RAG aspect didn't add much as it simply listed all 5 of the top books that were returned. With such a simple prompt, RAG doesn't seem necessary to provide a good recommendation for our users.

### `learn python programming beginner`

```
Based on the Amazon dataset, I would recommend the following books for learning Python programming as a beginner:

1. **"101 Extra Python Challenges with Solutions / Code Listings"** by  - This book provides a comprehensive collection of 101 Python challenges that help you develop and apply your programming skills. The book is well-structured and organized into ten chapters, making it easy to follow and understand.

2. **"40 Algorithms Every Programmer Should Know: Hone your problem-solving skills by learning different algorithms and their implementation in Python"** by Imran Ahmad - This book is a great resource for beginners who want to learn algorithms and data structures in Python. It covers a wide range of topics, from fundamental algorithms to machine learning and cryptography.

Both of these books are highly rated (4.5 and 4.3 respectively) and are suitable for beginners. They provide a solid foundation in Python programming and will help you develop your problem-solving skills.
```

We noted in Milestone 1 that both the semantic and BM25 keyword searches struggled with the beginner aspect of this query. This seemed to continue with the hybrid retriever. As such, the RAG pipeline recommends two books which are relevant to programming in Python and growing one's skills, neither are actually beginner friendly and require a strong baseline.

### `overcoming grief after losing a loved one`

```
Based on the provided Amazon dataset, I recommend the following books for overcoming grief after losing a loved one:

1. **Anatomy of Grief: An Inspirational Guide to Surviving the Death of Your Child** by Barbara Repczynski (5.0 rating) - This book chronicles the author's personal journey of coping with the loss of a child and offers practical advice on how to move forward.
2. **30 Days toward Healing Your Grief: A Workbook for Healing** by Danielle Morris (4.4 rating) - This workbook offers a Christ-centered approach to healing from loss, providing daily reflections and inspirational stories to help readers navigate their grief.
3. **I'm Grieving as Fast as I Can: How Young Widows and Widowers Can Cope and Heal** by Linda Sones Feinberg (4.5 rating) - This book provides a guide for young widows and widowers, addressing the unique challenges they face in coping with the loss of a spouse.
4. **Gravity's Embrace: A True Unsolved Mystery Surrounding An Alaskan Pilot** by Cynthia Young Fackrell (4.6 rating) - While not exclusively focused on grief, this book explores the heartache of a missing loved one and offers a powerful story of hope and resilience.

These books offer a range of perspectives and approaches to coping with grief, and may be helpful for individuals seeking guidance and support after losing a loved one.
```

Here the Hybrid RAG pipeline seems to perform quite well. We noted in Milestone 1 that the semantic search did better than BM25 and with RAG we were able to return specific explanations for why each of the cited books might be relevant to a user with this query.

### `self-help book for managing anxiety and stress at work`

```
Based on the provided Amazon dataset, I recommend the following self-help books for managing anxiety and stress at work:

1. **Emotional Core Therapy** by Robert A. Moylan: This book focuses on understanding and processing emotions to achieve emotional balance and reduce stress. The author provides a step-by-step process to help readers manage relationship stress and achieve inner peace.
2. **Cognitive Behavioral Therapy: A Psychologist's Guide to Overcome Anxiety, Depression, & Negative Thought Patterns** by [Author Not Available]: Although the author is not listed, this book on cognitive behavioral therapy can help readers overcome anxiety, depression, and negative thought patterns, which can be highly relevant to managing stress at work.
3. **The Art of Calm: Relaxation Through the Five Senses** by Brian Luke Seaward: While this book is not specifically focused on work-related stress, it offers practical tips and strategies for achieving calm and relaxation, which can be applied to managing anxiety and stress in the workplace.

Please note that the dataset does not provide information about the specific work-related stress management books.
```

In Milestone 1, we saw that some of the returned titles were more relevant than others and that while several were anxiety and stress related, they were not necessarily focused on managing these at work. The Hybrid RAG Pipeline did an excellent job of recommending the best matches from the hybrid search while acknowledging that they were not 100% relevant to the query as we wanted it to.

### `historical novel about World War 2 from a civilian perspective`

```
Based on your request for a historical novel about World War 2 from a civilian perspective, I recommend the following books:

1. **BBC History Magazine: The Second World War Story** - This book offers a comprehensive and engaging account of World War 2 from a British perspective, providing a unique civilian view of the war.
2. **A High and Hidden Place: A Novel** by Michele Claire Lucas - This novel tells the story of Christine Lenoir, a young woman who embarks on a journey to uncover the truth about her family's past and the horrors they experienced during World War 2. The book offers a powerful and emotional account of the war from a civilian perspective.

Both of these books are highly rated and offer a compelling and thought-provoking reading experience.
```

Although the first book is not a novel, the Hybrid RAG pipeline does a better job of capturing the civilian, World War 2 perspective than either the BM25 or semantic searches did alone.

## Overall Reflections

Overall, I am pleased with the performance of the RAG workflow. It goes beyond the raw retrieval to provide some reasoning for the top returned books. In some cases, it was able to even acknlowedge that the retrived books didn't quite fit the prompt but offered an explanation how they might still be helpful.

A key limitation of the RAG workflow is that it is limited by which 5 books were returned by the hybrid retriever. This means that if neither the BM25 nor semantic retrievers were able to effectively capture all of the meaning of the query, the RAG chatbot was stuck with a limited and incorrect basis of knowledge from which to work. This limitation is twofold: the retrievers return only 5 books and we used limited sample (10,000) books from which they are working. Another limitation may be in our choice of LLM and use of the free tier. With only 8 billion parameters and a 6000 token per minute limit, we had to truncate some parts of the book descriptions, features, and reviews that we gave the LLM. Perhaps with a larger context window, the LLM's responses could be even more comprehensive.

