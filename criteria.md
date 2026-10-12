# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I test this with one query I've checked against the data ('vintage graphic tee
under $30'), run 5 times. A try where search comes back empty counts as a fail,
since I know a listing matches. I parse the query with regex, so the parse and
the search give the same result every try. The only parts that can change
between tries are the two model calls, and a run can still fail there, for
example if the rate limiter runs out of retries. I'm allowing one miss out of
five for that.

**note**
assumes regex parsing

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
The logic should point to this every time a query matches no listings; no
exceptions. This path stops right after search, so it never calls the model,
and nothing random can change the result.

---

## 3. The same item reaches every tool

For one matching query ('vintage graphic tee under $30') run 5 times, the same
listing title appears in all four places: the first search result,
`session["selected_item"]`, and the inputs of the `suggest_outfit` and
`create_fit_card` steps in the trace, in 5 of 5 tries.

**Why this target:**
The handoff is plain code moving a dict through the session, with no model
involved, so nothing varies between runs. A mismatch would mean a bug in my
loop, like arguments in the wrong order or reading the wrong session key, and
that bug would show up in every run, not occasionally. That's also why one
query run 5 times is enough. I compare titles because all 40 are unique and
they already show up in the run log and the trace.

---

## 4. Repeat runs don't reuse an opening sentence

For one matching query ('vintage graphic tee under $30') run 5 times, each fit
card's opening sentence matches no other card's, in 5 of 5 tries. The opening
sentence is the text before the first line break or the first period,
exclamation point, or question mark followed by a space, or the whole caption
if none of those appear. Sentences are compared ignoring capitalization, emoji,
and punctuation.

**Why this target:**
My prompt is identical every try, so the temperature (0.9) is the only thing
pushing the cards apart. If the model has a go-to opener, this is where it
shows up first, and that's the failure I actually care about. I ignore emoji
and punctuation because a stock opener with a different emoji at the end is
still a stock opener. The target is 5 of 5 because a shared opener fails both
tries that share it, so 4 of 5 can't happen.

---

## 5. A model outage stops the run with a message instead of crashing

With one character of `GEMINI_API_KEY` changed in `.env`, a matching query run
through `python run_eval.py` shows "stopped early" instead of "CRASHED", and
the message names the API key as the problem, in 5 of 5 tries.

**Why this target:**
The error handling should work every time, since there's no randomness in it.
`generate.py` turns every way the model can be unreachable (bad key, no
network, bad model name) into the same `ModelUnavailable` error, so one trigger
tests the one handler. A miss would mean the handler is missing or wraps the
wrong step. The query has to be one that matches, and the message has to name
the key, so an empty search can't pass this by accident.

**Note**
needs its own run. Use the broken key with --label outage and read only that row. Change the key back afterward, or every later run will fail too.

---

**note**
Criteria 1, 3, and 4 all use the same query. In scenarios.py, list it once each under criterion 1, 3, and 4 so each gets its own row in the run log.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->