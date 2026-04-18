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
