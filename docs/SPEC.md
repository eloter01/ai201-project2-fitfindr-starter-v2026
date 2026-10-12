**Show What You Know: FitFindr**  
Thrifting takes work. You search four apps, try to picture how a thing would go with what you own, and guess whether the price is fair. Most of that is looking things up and comparing them.

In this unit you'll build FitFindr, an agent that does some of it for you. Someone says what they want — "a vintage graphic tee under \$30, size M" — and the agent searches listings, works out what it would go with, and writes a caption for it.

Last unit you built a system that answers. This one acts. It picks which tool to run, in what order, based on what came back.

This project runs for two units. In this unit you build it and write down what "working" would mean. In the next unit you test it against that standard and fix something. Same repository both units. Don't delete it.

You had most of your acceptance criteria handed to you last time. This time you get two. You write three.

**Goals**  
By the end of this unit you'll be able to:

Write a tool spec that says what goes in and what comes out  
Build a loop that picks its next step from what the last step returned  
Carry information from one tool call to the next without asking the user twice  
Write acceptance criteria for a system whose behavior changes run to run

### **What proves you did the work**

Three things. If all three are in your repo, your submission is complete.

1. **criteria.md** — five numbered acceptance criteria, each naming a target.  
2. **README.md** — the five sections listed at the bottom of this page.  
3. **Your commit history** — at least four new commits, in the repo you'll submit again in the next unit.

### **Features**

#### **Required Features**

* **Three tools with named inputs and outputs.** These three are required. You may add more.  
  * search\_listings(description, size, max\_price) — searches the listings file and returns matches.  
  * suggest\_outfit(new\_item, wardrobe) — takes an item and a wardrobe, returns outfit ideas.  
  * create\_fit\_card(outfit, new\_item) — writes a short caption someone would actually post.  
*   
* **A planning loop with at least one branch.** When search\_listings comes back empty, the loop must stop and say so. It must not call the next tool with nothing.  
* **Session state across tool calls.** The item search\_listings found flows into suggest\_outfit on its own. The user does not type it again.  
* **A way to run it.** A command line script or a small web page. It has to work without you standing next to it.  
* **Five acceptance criteria.** Two are written for you. You write three and explain all five. Milestone 3 walks you through it.

**RUNNING.md in the repo is your reference for everything else** — every command, which command goes with which milestone, what each file does, and what to do when something breaks. Read it once now, and come back to it whenever you're stuck. You don't edit that file.

**Quote your queries with single quotes**, on every operating system: python app.py ask 'vintage graphic tee under \$30'.

In PowerShell, double quotes turn \$30 into a variable that expands to nothing — your query silently becomes vintage graphic tee under , you get results with no price ceiling, and nothing warns you. Single quotes are literal in PowerShell, bash and zsh alike.

**Two of this project's three tools call the model**, so one run of your agent sends several requests. That matters more in this unit than in the previous one: a few runs back to back while you're debugging can put you over the per-minute limit. The starter paces you — if you go too fast it waits a moment and tells you it's waiting. That pause is the starter doing its job, not a bug.

The starter also reuses answers to prompts it has already sent, so re-running the same query while you debug costs you nothing. The next unit's testing turns that off, because there you need the real variation.

### **Milestone 1: Read the data and run the starter**

Your tools will only be as good as your understanding of what they're reading. Ten minutes in the data file now saves an hour of confused debugging later.

* Read five or six listings all the way through and write down the field names. Those fields are what search\_listings has to filter on — you can't filter on something that isn't there.

python app.py fields                    *\# what a listing and a wardrobe item hold*  
python app.py listings \--full \-n 6      *\# six whole records*

*   
* data/listings.json is the file itself if you'd rather read it directly.  
* Look at the wardrobe shape — app.py fields prints it, and data/wardrobe\_schema.json is the full version. This is what suggest\_outfit receives. Note what an empty wardrobe looks like.  
* Run the starter and give it one query:

python app.py examples                  *\# queries worth trying*  
python app.py ask 'vintage graphic tee under \$30'

*   
* **Single quotes**, on every operating system — see the note in Setup. Nothing is built yet, so it will tell you the planning loop isn't built. That exact message **is** the correct starting position — you're checking that it runs, not that it works.

**Before you move on**

The starter runs. You can name three fields in the listings file from memory. Commit and push to your fork — that's your first of at least four new commits.

---

### **Milestone 2: Spec your three tools**

Write down what each tool takes and what it gives back, before you write it.

This feels like a delay. It isn't. A tool with a vague return value produces a loop that can't branch on anything, because there's nothing definite to branch on. Most broken agents are broken here.

* For each of the three tools, write four lines in your README under **Tool Inventory**:  
  * What it does, in one sentence.  
  * Each input: its name and its type. max\_price (float), not "a price."  
  * What it returns, specifically. "A list" is not enough. "A list of listing dicts, each with title, price, size, platform" is.  
  * What it returns when it has nothing to give. An empty list? An error string? Pick one and write it down.  
*   
* Write down the one branch your loop needs. Say it as a rule: *"If search\_listings returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to suggest\_outfit."*  
* Read your spec back and ask one question of it: could someone else build this tool from what I wrote, without asking me anything? If not, the gap is your next sentence.

**📍 Before you move on**

All three tools have inputs with types, a specific return value, and an empty-case answer. Your branch rule is written as a rule. Commit.

---

### **Milestone 3: Write your acceptance criteria**

Refer to docs/acceptance\_criteria.md for guidelines.


An acceptance criterion says what "working" means, specifically enough that someone else could check it. Not *"the agent handles errors"* — that's an opinion. *"When search returns nothing, the agent stops before calling the second tool, in 5 of 5 tries"* — that's a criterion. It names a number.

You're writing these **before you test anything**. In the next unit you find out how you did against a standard you set when you couldn't know the answer.

Missing your own targets in the next unit does not cost you points. Setting a target so easy you can't miss it does.

 **On AI tools:** don't ask a model to write your criteria. Ask it to attack them. *"Could someone check this without asking me what I meant?"* is a good question to put to a model. A criterion you didn't write is one you can't defend.

* Open criteria.md. Two criteria are already written:

1\. Given a query that matches at least one listing, the agent completes all  
   three tool calls and returns a fit card — in at least 4 of 5 tries.  
2\. Given a query that matches no listings, the agent stops before calling  
   suggest\_outfit and returns a message naming what to change — 5 of 5 tries.

*   
*   
* Write three more. One must be about **state**: how would you know the item search found is the same item the next tool received? One must be about **the fit card**: it calls a model, so the same input can give different words each time. What would make that acceptable? The third is yours.  
* Under each of the five, write a sentence or two on why that target and not a stricter one. *"I picked 4 of 5 because my search is a plain keyword match and some phrasings will miss"* is a real answer.

**Working on your own?** Paste all five into Claude (or whichever AI tool you're using) and ask:

*"Here are five acceptance criteria for a multi-tool agent. For each one, tell me exactly how you would test it using only what the sentence says. Don't suggest improvements — just tell me what you'd do."*

Any criterion it can't turn into a test is one a grader can't either. You still decide what to change.

**📍 Before you move on**

criteria.md has five numbered criteria. Each names a number or something a person could plainly observe. Each has a reason underneath. Commit.

---

### **Milestone 4: Build the three tools**

Build each tool on its own and test it on its own. Do not wire anything together yet.

Three untested tools joined by a loop is not three problems. It's one problem that looks like six, because you can't tell which layer is lying to you.

* Build search\_listings. All three tools live in tools.py, as stubs waiting for you. Use the loader in utils/data\_loader.py rather than reading the file yourself. Filter on all three inputs. Return an empty list when nothing matches — an empty list, not None and not a crash.  
* Build suggest\_outfit. This one calls the model through the adapter function in the starter. Handle the empty wardrobe: return general advice rather than failing.  
* Build create\_fit\_card. This calls the model too. Run it three times on the same item and read the three outputs. If they're word-for-word identical, it's one of two things: the starter is handing back an answer it already had, or the temperature setting is at zero. Both are near the top of config.py — CACHE\_ENABLED and TEMPERATURE.  
* Test each tool from a terminal before moving on. One command per tool, one line of output you read with your own eyes. Paste the three commands and their output into your README under **Sample Run**.

**🛑 If you're stuck**

One tool still broken after 40 minutes? Have it return a hardcoded example that matches your spec's return shape, and write a comment saying so.

That's not giving up. The loop is the graded part of this unit, and a stubbed tool with the right shape lets you build it. In the next unit you'll have something concrete to diagnose.

**📍 Before you move on**

Each tool runs from the terminal and returns what your spec said it would, including its empty case. Commit.

---

### **Milestone 5: Wire the loop and the state**

Now connect them. The test that matters here is whether your agent behaves differently for different inputs.

If it calls all three tools no matter what comes back, you have a list of function calls. A loop looks at the last result before choosing the next step.

* Open agent.py. The session dictionary is already there. Fill in run\_agent() following your branch rule from Milestone 2\.  
* After each tool call, put its result in the session. Then read it back out of the session for the next call. Don't pass values straight from one call into the next — going through the session is what makes the state visible and testable.  
* Run the happy path. Print the session at the end. Check that the item in session\["selected\_item"\] is the same one that reached suggest\_outfit.  
* Run a query that matches nothing. Check that session\["fit\_card"\] is still None and that the message names what the user could change. "No results" is not that message.

**Working on your own?** Paste the message into Claude and ask:

*"Here is the message an app shows me when my search returns nothing. I know nothing about how the app works. Tell me what I would try next after reading it. If the honest answer is that I'd have no idea what to try, say that. Don't rewrite the message for me."*

If it comes back with nothing to try, the message isn't finished. What it should say instead is yours to work out.

**🛑 If you're stuck**

Loop not branching after 40 minutes? Print the value your branch checks, on the line right before the if. Nine times out of ten it isn't what you assumed — an empty string instead of an empty list, or a dict where you expected a list.

Still stuck after that? Commit what you have and write down what the printed value actually was. That's a real finding, and it's the next unit's diagnosis.

**📍 Before you move on**

A full query runs through all three tools with values moving through the session. An impossible query stops early with a useful message. Commit.

---

### **Milestone 6: Write it up and submit**

Most of your README is already written — you filled sections in as you went. This finishes it.

* Fill in **What This Does** and **How I Used AI**.  
* For **Planning Loop**, write the branch rule and name the file and function that holds it. The grader checks your code against what you claim here, so agent.py::run\_agent is what that line should look like.  
* For **How I Used AI**, describe two specific moments. What you asked, what came back, what you changed. *"I gave Claude my search\_listings spec. It returned None on no match instead of an empty list, so I changed it"* is the level of detail we want.  
* Check the repo: criteria.md is there, the README has all five sections, four new commits or more. Push everything to your fork, then submit **your fork's URL** — not the CodePath starter's.

**📍 Before you move on**

Your repository URL is submitted. **Write it down somewhere you'll find it in the next unit**


**How to Write Acceptance Criteria**

An acceptance criterion is a sentence that says what "working" means for your system, specific enough that someone else could check it without asking you what you meant.

You'll write five of them for every project in this course, and you'll write them **before** you know how your system does. That order is the whole point. Anyone can decide their system is good after seeing the results.

This is the central skill of the course. It's also the thing an interviewer is actually probing when they ask how you know your project works.

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

**✅ The criterion was broken.** You couldn't measure it, or it measured the wrong thing. Noticing that is a real finding and it earns points.

*"I couldn't judge 'relevant' the same way twice, so I changed it to whether the top three results contain the answer."*

**❌ You missed the number.** The criterion was fine; the system didn't clear it. That target stays exactly where it is.

*"I said 4 of 5 but got 2 of 5, so 2 of 5 is actually fine for my corpus."*

The test: is the problem with the **measurement**, or with the **result**?

When you do revise, the original line stays and the new one goes underneath with a reason. Never delete or edit what you wrote first — the record of what you believed before you knew the answer is the point.

**Before you commit to your five**

Run them through the [criteria self-check](https://courses.codepath.org/courses/ai201/pages/criteria_self_check). It takes about two minutes and catches most of the problems on this page.

 

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

**If nobody's around**

Paste your five into Claude and ask it to run this page against them:

*"Here are five acceptance criteria. For each one, answer these three questions: How exactly would you test it using only the sentence itself? Would two different people score it the same way? What would have to happen for it to fail? Don't rewrite them for me."*

That last instruction matters. A criterion an AI wrote for you is one you can't defend when someone asks where the number came from — and someone will.

 


