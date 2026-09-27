# The Unofficial Guide

---

# Unit 1

## What This Does

I chose the campus_life corpus. It contains short review documents about topics in
campus life, such as dining and housing. The corpus has 88 documents, each averaging
317 characters (shortest 178, longest 549). Each document follows the same structure:
a heading line, followed by two paragraphs of a few short sentences each.

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:**
Since the campus_life corpus contains 88 short review documents, each with a heading followed by two short paragraphs of review text, I chose a chunking strategy based on paragraph breaks, removing the heading line, which resulted in 183 chunks averaging 137 characters (shortest 36, longest 373). This is better than the default chunking strategy, which produced 88 chunks — essentially one per document — since splitting by paragraph lets retrieval surface the specific paragraph relevant to a question rather than the whole review.

**Overlap:**
Since my chunking strategy splits on paragraph breaks, I didn't use any overlap between chunks.


<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#1` — produced by: `chunker.py::split_documents`

```
Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`

```
The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
When will the sandwiches be restocked after picked clean after 1:15pm weekdays in the Atrium Dining Hall?

**Answer:**

```
(best distance 0.334, cutoff 0.5)

After being picked clean, the sandwiches are not restocked again until the next morning (dining_the_atrium.txt and dining_the_atrium_followup.txt).

Sources retrieved: dining_north_kitchen_followup.txt, dining_pellew_dining_hall_followup.txt, dining_the_atrium.txt, dining_the_atrium_followup.txt
```

**My relevance cutoff:**
0.5
<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| Which dining hall is the furthest from anywhere? | Yes | 0.3991 |
| Which dining hall serves grab-and-go refrigerated sandwiches? | Yes | 0.4756 |
| When will the sandwiches be restocked after picked clean after 1:15pm weekdays in the Atrium Dining Hall? | Yes | 0.3339|
| What worth knowing about the salad bar in Kestrel Commons after 1:30pm? | Yes |0.4208 |
| Which dining hall opens till midnight? | Yes | 0.4275 |
| What is the capital of Mongolia? | No | 0.8641 |
| How do I change the oil in a diesel engine? | No | 0.9106 |
| Who won the 1994 World Cup? | No | 0.8736 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8243 |
| How do I write a for loop in Rust? | No | 0.8313 |

As shown in the table, there is a clean gap between the in-corpus max (0.4756) and out-of-corpus max (0.8243). 

I would like to set the cutoff at 0.5, which separates both clusters.and their distances are not so well (0.47) compared to others (eg. 0.33).


## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I asked Claude for a suggested cutoff, and it recommended 0.6. However, all 5 of my
in-corpus questions had best distances between 0.33 and 0.47, so I set the threshold
to 0.5 instead — close enough to my actual in-corpus range that it should still catch
relevant chunks, with less margin for an unrelated question to slip through.

**2.**
I asked Claude to write a chunking function that splits text by paragraph, then added
logic myself to skip the first paragraph since it's the heading. I also asked Claude
to help revise my five criteria and the reasoning behind them.

**3.**
I asked Claude to explain why my first fix for Q5 was still failing and to suggest further fixes.

**4.**
I asked Claude about the Hybrid Search (BM25) approach, having it explain beforehand why it might fix the issue, then explain afterward why it didn't fully resolve it.


---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. No chunk is under 20 characters| 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Every answer comes back in under 30 seconds| 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->
Example output from one of the runs:

### When will the sandwiches be restocked after picked clean after 1:15pm weekdays in the Atrium Dining Hall? — run 2

- Best distance: 0.3339 (passed the gate)
- Sources retrieved: dining_north_kitchen_followup.txt, dining_pellew_dining_hall_followup.txt, dining_the_atrium.txt, dining_the_atrium_followup.txt

```
The sandwiches will not be restocked again until the next morning. 

Sources: `dining_the_atrium.txt` and `dining_the_atrium_followup.txt`
```



## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Out of the 5 questions, the retrieved chunk failed to answer only 1. The other 4 all contained the answer. So this criterion is met.|
| 2 | Every answer names a source | MET | All the answers come with naming a source. So this criterion is met.|
| 3 | Gate stops out-of-corpus questions | MET | For all 5 out-of-corpus questions, gate stops giving answers. So this criterion is met. |
| 4 | No chunk is under 20 characters | MET | Checking on the chunk size revealed that all chunks are between 36 and 373 characters long. So this criterion is met.  |
| 5 | Every answer comes back in under 30 seconds | MET | 3 runs come back together in under 30 seconds. So this criterion is met. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->
All criteria were met except the first one — "retrieved chunk contains the answer" — which missed 1 out of 5 questions. I investigated the cause.

For the question "Which dining hall opens till midnight?", the model responded that it didn't have enough information to answer, instead of returning the dining hall's name.

Diagnosis of the retrieved chunks:

Question: Which dining hall opens till midnight?

Root cause: The chunking strategy is dropping the first header line during chunking, causing later chunks to lose their contextual identity. In this case, the relevant chunk — "Hours are 11:00am to 1:00am daily during term. Costs declining balance, or cash after 11:00pm." — comes from the Verril Street Grill document, but since it doesn't mention the hall's name directly, it embeds farther away from the query than other, more generic chunks that do mention hall names explicitly.

|No | distance  | source |  preview|
|---|---|---|---|
|1|   0.4275 |    dining_halden_hall_followup.txt | Adding to what people have said about Halden Hall. T...|
|2 |  0.4279  |   dining_pellew_dining_hall_followup.txt| Adding to what people have said about Pellew Dining ...|
|3 |  0.4310 |    dining_north_kitchen_followup.txt |Adding to what people have said about North Kitchen....|
|4 |  0.5171 |    dining_the_atrium_followup.txt |  Adding to what people have said about The Atrium. Th...|
|5  | 0.5262  |   dining_halden_hall_followup.txt|  Also worth saying: closes at 7:00pm, which catches p...|

The top 4 retrieved chunks were mostly generic filler text, such as "Adding to what people have said about X." These chunks cluster closely in the embedding space around general "dining hall + closing time" language.

Interestingly, out of the 5 questions asked, two others (Q1 and Q2) were also "which dining hall" type questions, and both returned correct answers. Looking more closely at the retrieved chunks and source documents for those two, I found that both documents included the phrase "Adding to what people have said about X," but explicitly named the dining hall within the content — even though the header/title had been dropped during chunking.

By contrast, for Q5, the chunk containing the relevant answer information does not name the specific dining hall anywhere in its content. As a result, the model had no way to generate the correct answer from the retrieved chunks alone.



## The Improvement

**What I changed:**

To fix this, I propose prepending the dining hall name (from the title/header line) to every chunk, instead of discarding it during chunking.

**Why I picked it:**

This ensures each chunk retains its association with the correct dining hall name, so relevant context isn't lost even when chunks are split apart from their original headers.
<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->
| Question | Best distance (Before)| Best distance (After Title Prepend) |
|---|---|---|
| Which dining hall is the furthest from anywhere? | 0.3991 | 0.247 |
| Which dining hall serves grab-and-go refrigerated sandwiches? | 0.4756 | 0.449 |
| When will the sandwiches be restocked after picked clean after 1:15pm weekdays in the Atrium Dining Hall? | 0.3339 | 0.299 |
| What worth knowing about the salad bar in Kestrel Commons after 1:30pm? | 0.4208 | 0.273 |
| Which dining hall opens till midnight? | 0.4275 | 0.400 |


### Verdicts
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. No chunk is under 20 characters | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Every answer comes back in under 30 seconds | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |


**Did it help?**

This change significantly improved the best distances, especially for Q1, Q3, and Q4, as shown in the before/after comparison above. However, Q5 still failed across all 3 runs even after title prepending during chunking.
<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken
Q5 still failed across all 3 runs — the model continued to return that it had no information to answer the question. After examining the retrieved chunks, the top results were chunks listing open/close times in general, but not the one containing the correct answer.

Question: Which dining hall opens till midnight?

| No | distance |source  |                         preview|
|---|---|---|---|
|1  | 0.4001  |   dining_halden_hall_followup.txt | Re: Halden Hall: Also worth saying: closes at 7:00pm...|
|2  | 0.4448  |   dining_halden_hall.txt   |        Halden Hall: Hours are 7:30am to 7:00pm weekdays, cl...|
|3 |  0.4538  |   dining_halden_hall_followup.txt | Re: Halden Hall: Adding to what people have said abo...|
|4  | 0.4589  |   dining_north_kitchen_followup.txt| Re: North Kitchen: Adding to what people have said a...|
|5  | 0.4718  |  dining_pellew_dining_hall_followup.txt| Re: Pellew Dining Hall: Adding to what people have s...|

The top retrieved chunks were still generic filler text, such as "Adding to what people have said about X." which contains "dining hall + opening/closing time" language.

## Rephrase the query to near-vertatim match
I then tried rephrasing the query as "which dining hall hours are from 11:00am to 1:00am daily during term?" — containing a near-verbatim match to the answer string ("11:00am to 1:00am daily during term"):

| No | distance |source  |
|---|---|---|
|1 | 0.3545 | Halden Hall: Hours are 7:30am to 7:00pm weekdays...|
|2  |0.3983 | Pellew Dining Hall: Hours are 7:00am to 8:00pm daily...|
|3 | 0.4221|  The Atrium: Hours are 8:00am to 6:00pm weekdays... |

Even then, the correct chunk — despite containing an almost word-for-word match to the query — ranked 19th, at a distance of 0.594, above the gate's 0.5 cutoff, while the other generic filler text still ranked higher. So gate.py correctly refused to answer: nothing that passed the cutoff actually supported a valid answer.

**Root cause**: Why the title fix didn't solve Q5: the failure isn't a missing-context problem — it's a vocabulary/semantic-gap problem in the embedding model itself.

all-MiniLM-L6-v2 is a small, general-purpose bi-encoder. It's good at topical/lexical similarity, not at temporal reasoning: it has no strong basis for treating "1:00am" as close to "midnight," or "opens till midnight" as a paraphrase of "Hours are ... to 1:00am." Meanwhile, the top-ranked chunks — Halden Hall closing at 7pm, Pellew "Dining Hall" (matching on its own name), generic "Adding to what people have said..." filler — win purely because they share more surface vocabulary with the query ("dining hall," "hours," "closes/opens"), regardless of whether their actual answer is anywhere close to correct.

So this is a real limitation of the embedding model on numeric/temporal paraphrase, not a pipeline bug.


## Fix attempt: Hybrid search
To address this, I added keyword search (BM25) and combined it with semantic search via hybrid_store.py::search.

This combines the existing semantic search (store.py::search, cosine distance over all-MiniLM-L6-v2 embeddings) with a new keyword search (bm25_store.py::search, BM25 over tokenized chunk text). The two rankings are merged using Reciprocal Rank Fusion: each chunk earns a score of 1/(RRF_K + rank) from each retriever it appears in, and these are summed and then scaled against the best possible score (rank 1 in both lists), keeping the result interpretable across different questions. The fused score is not a cosine distance, even though it follows the same convention (0 = best possible, 1 = worst) — it requires its own gate cutoff, config.HYBRID_THRESHOLD, calibrated separately from config.THRESHOLD. It's enabled via --mode hybrid on app.py retrieve / app.py ask.

This directly addresses the gap identified in testing: several documents share a near-identical templated sentence, which the embedding model barely distinguishes since it captures overall meaning rather than exact numbers. BM25 catches these cases by scoring exact term overlap — for example, it correctly ranks the chunk containing "1:00am" first for a query naming that exact time, whereas semantic search alone had ranked it 19th out of 183.

However, Q5 still fails in the hybrid mode.


<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

Switching to a hybrid approach (adding BM25 keyword search alongside the embeddings) helps but doesn't fully fix it. Reciprocal Rank Fusion can still favor a chunk that ranks moderately well in both retrievers over one that's the clear #1 match in only one of them — it rewards consistency across both signals rather than a single confident hit. For Q5 specifically, the correct chunk was BM25's top match but ranked poorly in the semantic list, so the fused score lands below a chunk that placed second in both.

To surface it in the fused top-5, a few knobs are worth trying later: lowering RRF_K (which sharpens how much a rank-1 hit dominates over a rank-19 hit), widening fetch_k/top_k for hybrid mode, or moving to a weighted fusion that favors BM25 over the embedding for queries like this one.



<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
