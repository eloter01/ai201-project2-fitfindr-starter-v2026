## **Show What You Know: FitFindr, Part 2 — Testing**

In the previous unit, you built an agent and wrote down what "working" would mean for it. You filed those five criteria before you had any results.

In this unit you find out how you did.

You'll also do two things your agent has never had done to it. You'll move one tool onto **MCP**, a standard way of exposing a tool so any agent can call it. And you'll break each tool on purpose, to see what the agent says when something fails.

Then you run your criteria, call each one, work out why the misses happened, fix one thing, and run again. Same repository, same URL.

**Missing your own targets does not cost you points.** An agent that misses every criterion, with a clear explanation of each miss, earns full marks. What's graded is whether you tested honestly. Passing a test unit doesn't open anything up, and failing one doesn't hold you back.

Read that twice, because the instinct in this unit is to make your agent look good. A criterion quietly loosened until it passes leaves you nothing to diagnose, and the diagnosis is where the points are.

### **Goals**

By the end of this unit you'll be able to:

* Move a tool behind MCP so something other than your own code can call it  
* Trigger a failure on purpose instead of waiting for one  
* Test a system with repeated tries, not one lucky run  
* Trace an agent's decisions and say why it chose each step

### **What proves you did the work**

Three things, added to the repo you submitted in the previous unit.

1. **A run log** — your five criteria, five tries each, before your fix and after it.  
2. **A verdict and a diagnosis** — met or missed per criterion, and what caused every miss.  
3. **A loop trace** — one full run printed step by step, with the MCP tool call visible in it.

### **Features**

#### **Required Features**

* **One tool moved onto MCP.** Pick one of your three. Your agent calls it through MCP from then on. The other two stay as they are.  
* **Every failure mode triggered on purpose.** Three of them, listed in Milestone 2\. Each one gets a handler that tells the user what broke and what to try.  
* **A trace of one full run.** Every tool call in order, with what went in and what came back.  
* **Five tries per criterion.** One run isn't a test. Two of your tools call a model, so the same input can give different answers. Your criteria name a target out of five, so five tries is what it takes to score one.  
* **A verdict and a diagnosis for each of your five criteria.** Met or missed against the previous unit's target, and for every miss, which tool and which step. "It got it wrong" isn't a diagnosis.  
* **One improvement, made and measured.** Change one thing, run the test again, put both results side by side

**One rule about changing your system.** The MCP move and your one improvement are the only changes in this unit. Everything else stays. It's the same agent, not a second one. 

RUNNING.md in your repo still has every command, every flag, and the troubleshooting table. One entry there is worth knowing now: IncompleteFieldDefinitionWarning: Field 'lifespan' is harmless noise from the MCP library's dependencies, not your code and not an error.

**One thing does change for testing.** While you were building, the starter reused answers to prompts it had already sent. Testing turns that off, because five tries of the same question are only worth running if the model actually answers five times. That means a test run sends more requests than a build run did, so expect the starter to pause and pace itself more than it used to. Let it.

### **Milestone 1: Move one tool onto MCP**

Right now your tools only exist inside your program. Nothing else can reach them. MCP is a shape you wrap a tool in so that anything speaking the same protocol can call it — your agent today, a different agent tomorrow, someone else's app after that.

You're moving one tool. Not three. The point is to see the seam.

* Pick the tool to move. search\_listings is the easiest, because it doesn't call a model.  
* Open mcp\_server.py. It's already there with a commented-out template waiting. Register your tool with its name, a one-line description, and its inputs. The input names and types come straight from your Tool Inventory — if they don't match your README, fix whichever one is wrong.  
* Check the server offers what you think it does — python mcp\_client.py asks it and prints the answer. If your tool isn't listed, nothing registered.  
* Point your agent at the server as a client: swap the direct call in run\_agent() for mcp\_client.call\_tool, then run one query end to end. The call changes shape; what it returns should not. If the result differs from the previous unit, that difference is your first clue about what your tool was really returning before.

MCP not connecting after 40 minutes? Stop. Keep your direct call, and write down in your README exactly where it broke — the error text, and the last thing that worked.

Then carry on to Milestone 2\. Everything after this milestone works with a direct call, and a documented failure you can describe is a complete submission.

**Before you move on**

One tool runs through MCP and a normal query still works. Or you have a written record of where it stopped. Commit either way.

### **Milestone 2: Break it on purpose, then trace it**

Trigger each failure yourself. Don't wait to find out in a graded run.

Then print a trace. Most people can describe what their agent does. Far fewer can show it. A trace is the difference, and your diagnosis in Milestone 4 depends on having one.

* Trigger all three failures, one at a time, and write down what your agent said each time:  
  * **Empty search.** Query something your data can't possibly have. The agent should stop and name what to change.  
  * **Empty wardrobe.** Run with python app.py ask '...' \--empty-wardrobe, which hands suggest\_outfit a wardrobe holding no items. It should return advice, not a crash and not an empty string.  
  * **Model unavailable.** Change one character of your key in .env, then run a query **you haven't asked before**. The agent should say the model couldn't be reached — not hang, and not show a raw stack trace. A query you've already run is answered from the build cache without calling the model, so it can't show you this failure; if the last line says "served from cache", that's what happened. Put the key back when you're done.  
*   
* For any of the three that crashed or went silent, add a handler. Each message names what broke and what the user can do.  
* Add a trace. One trace.step() call per step, giving the tool name, the inputs, and what came back — trace.py handles the formatting, you decide where the calls go. Then run one full query with python app.py ask '...' \--trace and paste the trace into your README under **Loop Trace**. If \--trace prints nothing, you haven't added the trace.step() calls yet.

**If you're stuck**

Can't get a failure to trigger? Force it. Put return \[\] at the top of the tool, run the agent, then take it out. Faking the failure to test the handler is a normal thing to do.

**Before you move on**

All three failures have been triggered and each produces a message you'd be willing to show a user. Your trace is in the README. Commit.

### **Milestone 3: Run your test**

Run each of your five criteria five separate times, and write down what happened.

Five tries, not one. Your criteria name a target out of five — "4 of 5", "5 of 5" — so five is exactly what it takes to score one of them. You cannot tell a 5-of-5 agent from a 3-of-5 agent in a single pass.

* Work out what each criterion needs you to run, and put those scenarios in scenarios.py — that file is what run\_eval.py executes. Three scenarios ship filled in to show the shape; the rest are yours, and the ones there are a starting point rather than a fixed set. A criterion about the empty-search branch needs an impossible query. One about the fit card needs the same item run more than once. Set each scenario's criterion key to the number in criteria.md it tests, so the run log's rows line up with your run-log table.  
* Run everything five times. python run\_eval.py \--label before does exactly this — every scenario, five times, with caching off. Same inputs, same agent, nothing changed in between. Save the real output — you'll paste some of it in later.  
* Fill in your run log. Every test unit in this course uses the same format — one row for **each of your five criteria**, a column per try, and a verdict. A table with fewer than five rows isn't a complete run log:

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |  
|---|---|---|---|---|---|---|---|  
| 1\. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | FAIL | PASS | FAIL | MISSED (3/5) |  
| 2\. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |  
| 3\. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |  
| 4\. Fit card mentions the item's price | 5 of 5 | PASS | PASS | PASS | FAIL | PASS | MISSED (4/5) |  
| 5\. Over-budget query returns nothing over the limit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

*   
*   
* Under the table, paste real output for each criterion from one try. The actual text, not a description of it. Name the file and function that produced it.

**Before you move on**

Your run log has five criteria, five tries each, with pasted output underneath. Commit.

If all five tries came out identical on a criterion that involves a model, check two things: that you're really re-running, and that you're running in test mode — in build mode the starter hands back answers it already had.

---

### **Milestone 4: Call each criterion and diagnose every miss**

Say met or missed against the target you wrote in the previous unit. Then work out why the misses happened.

Calling them sounds like the easy part. It's the part people get wrong, because "met" is more comfortable and there's always a generous reading. Read them plainly instead.

* Write MET or MISSED next to each criterion. Count the passes across your five tries and read that count against the target. If your target said 4 of 5 and you passed 3, that's a miss — and passing 4 is a miss too when the target said 5 of 5\. The target has to hold, not turn up sometimes.  
* For each miss, name the **step** and the **mechanism**. Your agent has four places to fail: a tool, the loop's branch, the session, or the model's output.  
  **Not a diagnosis:**  
  "The fit card was bad."  
  **A diagnosis:**  
  "The fit card criterion missed on 2 of 5 items. Both were items with an empty brand field. My prompt puts the brand in the first sentence, so the card opened with a blank and read like a fragment. The tool worked; the prompt assumed a field that isn't always there."  
* Look for a pattern. If three misses all involve the same tool, that's one problem, not three. Patterns are worth more than individual explanations. If you missed nothing at all, say so — then say honestly whether your targets were low, and name the criterion you'd tighten.

**A note on changing a criterion**

Sometimes a criterion turns out to be broken rather than unmet. That's a real finding and it earns credit. Only one kind of change counts.

**This earns points.** The criterion couldn't be measured, or measured the wrong thing:

*Original: "The fit card is different every time."* *Revised: "For 5 different items, the 5 fit cards share no opening sentence."* *Why: "different" wasn't checkable — two cards that differed by one word still counted. The new version is something I can actually score.*

**This does not.** The criterion was fine; you missed it:

*Original: "Empty search stops the loop 5 of 5 times."* *Revised: "Empty search stops the loop 3 of 5 times."* *Why: 3 of 5 turned out to be more realistic.*

* If you revise, leave the original line in place and put the new one underneath with your reason. Never delete the original.

**Before you move on**

Every criterion has a verdict and a sentence on how you decided. Every miss names a step and a mechanism. Commit.

### **Milestone 5: Fix one thing and re-run**

Pick one thing your diagnosis pointed at, change it, and run the whole test again.

One change, measured properly, beats four changes you can't tell apart.

* Pick your improvement. Common ones, in rough order of how often they help:  
  **Tighten a tool's return shape.** If your diagnosis found a missing or oddly-typed field, fix the tool to always return the shape your spec promised.  
  **Add a second branch.** If a failure walked straight past your single branch, add the check that would have caught it.  
  **Rewrite one prompt.** If a model-calling tool produced something unusable, change what you send it — and say what you changed.  
  Or something else your diagnosis named. Follow the diagnosis, not this list.  
* Make the change, then run the full test again — python run\_eval.py \--label after, five criteria, five tries each, same format. One change only. If you're fixing three things, stop and pick the one your diagnosis actually named.  
* Put both run logs in your README, before and after, so the difference is visible side by side.  
* Say whether it helped. **If it didn't, say that.** A change that made things worse, honestly reported, earns full credit and is more interesting than one that worked.

**If you're stuck** 

Keep what you have, put both run logs in anyway, and write down what you tried and where it broke.

A failed improvement you can explain is a complete submission. An unfinished one you can't describe isn't.

**Before you move on**

Both run logs are in your README. You can say in one sentence whether the change helped. Commit.

### **Milestone 6: Say what's still broken, and submit**

Finish the write-up and make the call on what you didn't fix.

* Write **What's Still Broken**. For each criterion still missed: what you'd do, and why you stopped there. "I ran out of time" is fine if it's true. Pretending nothing is left is not.  
* Add a line on the MCP move: what changed in your code, and whether anything behaved differently after.  
* Update **How I Used AI** with anything from this unit, then submit the **same URL you submitted in the previous unit**.

**Before you move on**

Both run logs, a verdict per criterion, your diagnoses, your trace, and your call on what's left. Same repository URL. Commit.

