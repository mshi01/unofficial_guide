# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

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
**Overlap:**
The campus_life corpus contains 88 short review documents, each with a heading followed by two short paragraphs of review text. I chose a chunking strategy based on paragraph breaks, removing the heading line, which resulted in 183 chunks averaging 137 characters (shortest 36, longest 373). This is better than the default chunking strategy, which produced 88 chunks — essentially one per document — since splitting by paragraph lets retrieval surface the specific paragraph relevant to a question rather than the whole review.

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
You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```
```

**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`
Start the term project in week three, not week eight; everyone learns this the hard way.
```
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`
People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
```
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#1` — produced by: `chunker.py::split_documents`
Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.
```
```

**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`
The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
When will the sandwiches be restocked after picked clean after 1:15pm weekdays in the Atrium Dining Hall?

**Answer:**
(best distance 0.334, cutoff 0.5)

After being picked clean, the sandwiches are not restocked again until the next morning (dining_the_atrium.txt and dining_the_atrium_followup.txt).

Sources retrieved: dining_north_kitchen_followup.txt, dining_pellew_dining_hall_followup.txt, dining_the_atrium.txt, dining_the_atrium_followup.txt
```
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
| When will the sandwiches be restocked after picked clean after 1:15pm weekdays in The Atrium Dining Hall? | Yes | 0.3339|
| What worth knowing about the salad bar in Kestrel Commons after 1:30pm? | Yes |0.4208 |
| Which dining hall opens till midnight? | Yes | 0.4275 |
| What is the capital of Mongolia? | No | 0.8641 |
| How do I change the oil in a diesel engine? | No | 0.9106 |
| Who won the 1994 World Cup? | No | 0.8736 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8243 |
| How do I write a for loop in Rust? | No | 0.8313 |

As shown in the table, there is a clean gap between the in-corpus max (0.4756) and out-of-corpus max (0.8243). 

I would like to put the cutoff at 0.5, which separates both clusters.

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
<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

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
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

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

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
