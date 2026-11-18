## **Capstone**

**Specs are in docs/final_SPEC.md**

We’re going to extend a system.

**B. Harden against failure.** Take a system that works when everything goes right and make it survive when things don't. Timeouts, retries, missing input, an API that returns nothing, a rate limit you hit. The extension is the failure handling, and your criteria are about what happens on the bad path.

**How we’ll run**

**local with logs.** Your system runs on your machine, started by a single documented command, with a committed record of it actually running. You include:

* The exact command that starts it, in RUNNING.md, tested from a clean checkout  
* A committed run record — your structured log from a real session, pasted as text  
* What the environment needs: Python version, the pinned dependencies, any model files and their size

**What we need**

**Build half**

1. **criteria.md** — five numbered acceptance criteria, all yours, written before you have results.  
2. **README.md** — the build sections listed at the bottom of this page, including which shape you picked and what's out of scope.  
3. **RUNNING.md** — the run path. A URL and how it got there, or the single command and the environment it needs.

**Test half**

4. **A run log** — your five criteria, three trials each, before your fix and after it.  
5. **A verdict and a diagnosis** — met or missed per criterion, and what caused every miss.  
6. **A cost measurement** — what one run costs, and how you worked that out.

### **required**

* **One system, extended.** Say which, and say what's new.  
* **One shape, declared.** We chose B., named in your README, with a sentence on what you decided is out of scope.  
* **A run path that isn't your editor.** **local with logs**. RUNNING.md holds it.  
* **Structured logging.** Every run writes a record with named fields — at minimum a timestamp, what came in, what came out, and how long it took. Pasted extract in the README, at least ten entries.  
* **A cost number.** What one run costs you: API spend, tokens, or seconds of compute. Measured, not estimated from the docs. Say how you got it.  
* **Five acceptance criteria.** At least three of the five must be about **the extension**, not about the system as it already worked.  
* **Three trials per criterion.** One run is not a test. Anything touching a model can come out differently twice.  
* **A verdict and a diagnosis for each criterion.** Met or missed against the target, and for every miss, which part of the system and how.  
* **One improvement, made and measured.** One change, re-run, both result sets side by side.  
* **A written call on what's left.** What you'd do, and why you stopped.

### **Milestone 1: Pick the system, pick the shape, cut the scope**

* Pick the shape: We picked B. Write one paragraph in your README under **The Shape** saying what you're adding.  
*   
* **Write what's out of scope.** Two or three things you thought about doing and decided not to. This is the part people skip and it's the part that saves the unit. *"I'm not adding a second retriever, I'm not touching the chunking, and I'm not rebuilding the interface"* is a real answer.

### **Milestone 2: Build the extension**

* Build it. One capability, one hardening layer, or the operational scaffolding — whatever your shape named.  
* Confirm the original system still works. An extension that breaks what it extends is a regression, and you'll find it faster now than in Milestone 5\.  
* Commit as you go. At least three commits in this milestone alone.

### **Milestone 3: Get it running, and make it observable**

* **Pick your path** —we chose local-with-logs — and write RUNNING.md. The exact start command and what the environment needs.  
* **Double check the instructions in** RUNNING.md  
* **Add structured logging.** Every run writes a record with named fields — timestamp, input, output, duration, and anything specific to your system worth knowing later. A file you can read back, not print().  
* **Log the failures too.** A run that errored should leave a record. A failure that shows up only as an absence is one you'll never find.  
* **Measure the cost of one run.** API spend, tokens consumed, or seconds of compute — whichever is the real cost for your system. Run it ten times, take the average, and write down **how you measured it**. A number from the pricing page isn't a measurement.  
* Paste at least ten log entries into your README under **Instrumentation**, and the cost number with its method under **What It Costs**. Also paste at least one failed run (an error, a timeout, or a rejected input) alongside the ten. If you tested the failure path and nothing failed, say that under the entries instead.

### **Milestone 4: Generate the criteria**

* Write five numbered criteria in criteria.md. **At least three must be about the extension**.  
* Give each one a target: a number, a rate, or something a person could plainly see. If the sentence turns on *works*, *reliable*, *good*, or *fast*, it isn't a criterion yet.  
* Under each, say why that target and not a stricter or looser one. The reason should reference something about your system or what being wrong would cost.  
* Make sure at least one of them is about **what happens when things go wrong** — an error, a timeout, an empty result, a bad input. Every system has a bad path, and it's where the interesting failures live.  
* Critique them against docs/[criteria.md](http://criteria.md)

### **Milestone 5: Run the test**

Work out what each criterion actually needs run against it, then run it.

* For each criterion, decide what has to be run to produce its number. A criterion about failure handling needs failures — trigger them deliberately. A criterion about latency needs enough runs to have a distribution rather than one number.  
* Run everything three separate times and save the real output. Then fill in the run log. Every test unit in this course uses the same format — one row for **each of your five criteria**, a column per run, and a verdict. A table with fewer than five rows isn't a complete run log:

```
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Deployed endpoint answers under 5s | 9 of 10 | 8/10 | 9/10 | 7/10 | MISSED |
| 2. Timeout returns a message, not a crash | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Every run appears in the log | 10 of 10 | 10/10 | 10/10 | 9/10 | MISSED |
| 4. Cost per run stays under $0.01 | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Malformed input gets a 400, not a 500 | 5 of 5 | 5/5 | 4/5 | 5/5 | MISSED |
```

*   
* Underneath the table, paste real output for each criterion from one of the runs — the actual log lines or responses, not a description of them. Name the file and function that produced it.

**📍 Before you move on**

Five criteria, three trials each, with pasted output underneath. Commit.

If a criterion involving a model came out identical three times, check you're really re-running.

### **Milestone 6: Call every criterion, diagnose every miss, fix one**

* Write MET or MISSED next to each criterion, against the target you set in Milestone 4\. If your target said 9 of 10 and your trials came out 8, 9, 7 — that's a miss. The target has to hold, not turn up sometimes.  
* For each miss, name **where** and **how**. You know your system's stages better than any brief could tell you — name the one that produced the failure and the mechanism that made it.  
  **Not a diagnosis:**  
  "It was slower than I expected."  
  **A diagnosis:**  
  "Three of ten runs came back over 5 seconds. All three had queries that matched more than twelve chunks, and my reranker scores every match serially before it truncates. The stage is the reranker; the mechanism is that its cost scales with match count, and my criterion assumed it scaled with result count."  
* Look for a pattern. If three misses all trace to the same stage, that's one problem with three symptoms, and saying so is worth more than three separate explanations. If you met all five, say so — then say honestly whether your targets were set low, and name the criterion you'd tighten and the target you'd tighten it to.  
* **Pick one improvement, make it, and re-run.** One. Follow the diagnosis — the fix should be aimed at something you just explained. Then run the full set again, three trials each, in the same format.  
* Put both result sets in the README, before and after, so the difference is visible side by side. Then say whether it helped. **If it didn't, say that.** A change that made one thing better and another worse, honestly reported with the trade named, earns full credit.

**A note on changing a criterion**

Sometimes a criterion turns out to be broken rather than unmet. That earns credit — but only one kind of change counts.

If you revise, leave the original line and put the new one underneath with your reason. Never delete the original. 

### **Milestone 7: Cost, what's left**

* Finish **What It Costs**. Your measured per-run number, how you measured it, and one sentence on what it would cost to run this for a hundred people a day. Show the arithmetic — it's multiplication, and the point is that you can produce the number rather than wave at it.  
* Write **What's Still Broken**. For each criterion still missed: what you'd do, and why you stopped. "I ran out of time" is fine if it's true. If you met all five, this section still isn't empty: say which target was set too low and what you'd tighten it to.  
* Add two sentences on what you'd do next if this were real and you had another unit. Not a wish list — the one thing you'd do first, and why that one.  
* Write a new **How I Used AI** under your \#\# Capstone heading (leave the earlier project's where it is), check the repo against the submission list below, and submit the URL.

**📍 Before you move on**

Both result sets, verdicts, diagnoses, the cost number, and your call on what's left. 

