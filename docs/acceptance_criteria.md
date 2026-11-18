**How to Write Acceptance Criteria**

An acceptance criterion is a sentence that says what "working" means for your system, specific enough that someone else could check it without asking you what you meant.

Acceptance criteria should be written **before** you know how your system does. That order is the whole point. Anyone can decide their system is good after seeing the results.

**What makes a criterion a criterion**

**It names a target.** A number, or something a person could plainly observe.

| Not a criterion | A criterion |
| :---- | :---- |
| "Retrieval works" | "For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer" |
| "Catches profanity" | "Catches profanity in at least 9 of 10 trials" |
| "Handles errors gracefully" | "When the search tool returns nothing, the agent says so and moves on instead of crashing — in all 5 of my triggered failures" |
| "The answers are good" | "Every answer names at least one source document" |

The pattern on the right is always the same: **a thing that happens, and how often it has to happen.**

**Two questions to ask yourself**

**Could someone else check this without asking me anything?**

If the answer is no, it isn't a criterion yet. "The chunks are the right size" fails this — right according to whom? "No chunk is under 40 characters or over 600" passes.

**Would I score it the same way on Monday and Wednesday?**

If a criterion uses a word like *relevant*, *useful*, *reasonable*, or *good*, you'll apply it differently depending on your mood. Replace the word with the thing you'd actually look at. Instead of "returns relevant results," try "the top three results mention the professor named in the question."

**Where the number comes from**

You don't need a number you can defend to a statistician. You need a number you can explain.

Good reasons for a target:

"I picked 4 of 5 because one of my questions is about a topic only two documents mention, so I expect that one to be hard."

"I picked 5 of 5 because this one is either working or it isn't — there's no reason to accept less."

"I picked 8 of 10 because I'd rather it refuse a few real questions than answer one it shouldn't."

Each of those says something about the system or the data. That's what a reason is for.

A bad reason is one that could apply to anything: *"80% seemed reasonable."*

**Aim for a real standard, not a safe one**

The temptation is to set targets you're sure you'll hit. Resist it, for a practical reason: **passing earns you nothing.**

Points come from criteria that are specific and testable, from a test that actually ran, and from a clear diagnosis of what failed. A criterion set low enough to pass produces nothing to diagnose — which costs you more than the failure would have.

Missing your own targets is not a problem. A system that misses every criterion, with a clear explanation of each miss, earns full marks. That's not a consolation prize; it's how the grading actually works.

So write the criterion you'd want to be true, not the one you're sure of.

**Five criteria, five different things**

Try to cover different parts of your system rather than five versions of one idea. For a retrieval system, that might be:

1. Something about **retrieval** — does the right material come back?  
2. Something about **the answer** — is it grounded, sourced, correct?  
3. Something about **failure** — what happens when there's nothing to answer from?  
4. Something about **your own design choice** — the chunking, the threshold, the thing you spent time on  
5. Something **you care about** — pick the thing that would embarrass you if it didn't work

The fifth one matters more than it looks. A criterion you're actually invested in gets tested honestly.

**Changing a criterion later**

You can revise a criterion in the test unit, but only one kind of change earns credit.

**The criterion was broken.** You couldn't measure it, or it measured the wrong thing. Noticing that is a real finding and it earns points.

*"I couldn't judge 'relevant' the same way twice, so I changed it to whether the top three results contain the answer."*

**You missed the number.** The criterion was fine; the system didn't clear it. That target stays exactly where it is.

*"I said 4 of 5 but got 2 of 5, so 2 of 5 is actually fine for my corpus."*

The test: is the problem with the **measurement**, or with the **result**?

When you do revise, the original line stays and the new one goes underneath with a reason. Never delete or edit what you wrote first — the record of what you believed before you knew the answer is the point.


**Criteria Self-Check**

Run your five criteria through this before you commit to them. Two minutes now saves a week of testing something you can't measure.

Use it on your own criteria, and use it when you're reviewing someone else's in your breakout.

**Check each criterion on its own**

For every one of your five, answer these. A **no** anywhere means rewrite it.

* **Does it name a number, or something a person could plainly see?** "9 of 10 trials" counts. "Reliably" doesn't.  
* **Could someone else check it without asking me what I meant?** Hand it to a person who has never seen your project. Could they tell what to do?  
* **Would I score it the same way on two different days?** If it turns on a word like *relevant*, *useful*, *reasonable*, or *good*, it will drift. Replace that word with the thing you'd actually look at.  
* **Does it describe one thing?** "Retrieval works and answers are grounded" is two criteria wearing one coat. Split it.  
* **Can I say why that number and not a stricter or looser one?** Your reason should say something about your system or your data. "80% seemed reasonable" isn't a reason.  
* **Is it about my system, not about me?** "I will test thoroughly" isn't a criterion. It doesn't describe anything the system does.

**Check the set as a whole**

* **Do the five cover different parts of the system?** Five criteria about retrieval leave the rest of your project untested.  
* **Is at least one of them about what happens when things go wrong?** Empty results, a question you can't answer, a tool that fails.  
* **Is at least one of them something I'd be genuinely disappointed to miss?** If every target is safe, the test unit has nothing to teach you.  
* **Would I be comfortable if a stranger tested my system against these?** This is the real question. If the honest answer is that they'd find something the criteria don't catch, add that thing.

**The rewrite pattern**

Most broken criteria fail in the same way and get fixed the same way.

| Start with | Ask | End with |
| :---- | :---- | :---- |
| "Chunks are the right size" | Right according to what? | "No chunk is under 40 characters or over 600" |
| "Handles errors well" | What would I see? | "When the tool returns nothing, the system says so instead of crashing — all 5 triggered failures" |
| "Answers are accurate" | How would I check? | "For 4 of 5 questions, the answer matches what the source document says" |
| "The system is fast" | Fast enough for what? | "Every answer comes back in under 30 seconds" |

The move is always the same: replace the judgment word with the thing you'd actually look at.

**If you're reviewing someone else's**

Ask them these three, in this order:

1. **Give me criterion 3, just the sentence.** No project background, no explanation of what they meant.  
2. **From that alone, how would I test it?** If you can't say, the criterion isn't done.  
3. **What would have to happen for this to fail?** If they can't picture it failing, the target is set too low.

That third question finds more problems than the other two combined.

 

