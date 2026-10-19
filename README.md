# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps you shop for thrifted clothes. You type what you want in plain
words, like 'vintage graphic tee under $30', and it searches 40 sample
listings from Depop, thredUp and Poshmark for the best match. Then it suggests
one or two outfits that pair the item with clothes you already own, and writes
a short caption you could post about the find. If nothing matches, it stops
and tells you what to change in your search.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Finds listings that match the user's words, and filters
  them by size and price when those are given. It doesn't call the model.
- **Inputs:** `description` (str): keywords like `"vintage graphic tee"`.
  `size` (str or None): a size like `"M"`, `"US 8"` or `"W30"`, or None to
  skip the size filter. `max_price` (float or None): the highest price
  allowed, inclusive, or None to skip the price filter.
- **Returns:** A list of listing dicts, best match first, at most 10
  (`config.SEARCH_RESULT_LIMIT`). Each dict has all 11 listing fields: `id`,
  `title`, `description`, `category`, `style_tags` (list), `size`,
  `condition`, `price` (float), `colors` (list), `brand` (str or None),
  `platform`.
- **When it has nothing:** Returns an empty list `[]`, never None, and doesn't
  raise. This happens when no listing passes the size and price filters, or
  when none shares a word with the description.
- **How it ranks:** Each word in `description` scores 1 point if it appears as
  a whole word in the listing's title, description, category, style_tags or
  colors. Case doesn't matter. Filler words like "a", "in", "for", "looking"
  and "size" are skipped, because "a" alone appears in 18 of the 40 listings.
  One-character words, like the "8" in "size 8", are skipped too. Listings
  that score 0 are dropped. Higher scores come first, and ties keep the order
  of the listings file.
- **How sizes match:** Any listing whose size includes "One Size" passes the
  size filter, since it's made to fit everyone. For the rest, anything in
  parentheses is dropped and each size is split on `/` into options, so `S/M`
  becomes `S` and `M`, and `XL (oversized)` becomes `XL`. A listing matches if
  it shares at least one option with the requested size, ignoring case. So `M`
  matches `S/M` and `M/L`, `L` does not match `XL`, `S` does not match
  `US 9`, `US 8` does not match `US 8.5`, and `W30` does not match `W30 L30`.

### `suggest_outfit`

- **What it does:** Asks the model, through `generate()`, for one or two
  outfits that pair the new item with clothes the user already owns. The
  prompt uses the item's title, category, colors and style_tags. It doesn't
  use `brand`, since only 8 of the 40 listings have one.
- **Inputs:** `new_item` (dict): one listing dict from `search_listings`.
  `wardrobe` (dict): `{"items": [...]}`, where each item has `id`, `name`,
  `category`, `colors` (list), `style_tags` (list) and `notes` (str or None).
- **Returns:** A non-empty string with one or two outfit ideas in plain text.
  Each outfit names the wardrobe pieces it uses by their `name`, like
  "Baggy straight-leg jeans, dark wash".
- **When it has nothing:** If `wardrobe["items"]` is empty, it returns general
  styling advice for the item instead of naming owned pieces. A `wardrobe` of
  None is treated the same way. If the model sends back empty text, it returns
  a short message saying no outfit could be suggested. It never returns `""`
  or None. If the model can't be reached, it raises `ModelUnavailable`, which
  `run_agent` catches. If `new_item` isn't a non-empty dict, it raises
  `ValueError`, since there's nothing to style.

### `create_fit_card`

- **What it does:** Asks the model, through `generate()`, to write a short
  caption someone would actually post about the find, based on the outfit
  suggestion.
- **Inputs:** `outfit` (str): the text `suggest_outfit` returned. `new_item`
  (dict): the same listing dict that went into `suggest_outfit`.
- **Returns:** A string with a casual caption of 2 to 4 sentences. It mentions
  the item, its price and its platform once each. The wording changes from run
  to run.
- **When it has nothing:** If `outfit` is empty, only whitespace, or None, it
  returns a message saying there's no outfit to write about, without calling
  the model. If the model sends back empty text, it returns a message saying
  the caption couldn't be written. It doesn't raise in either case. If the
  model can't be reached, it raises `ModelUnavailable`, which `run_agent`
  catches. If `new_item` isn't a non-empty dict, it raises `ValueError`.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in
`session["error"]` that says what the user could change (broader words, a
different size, or a higher price), and return the session without calling
`suggest_outfit`. Otherwise, put the first result in `session["selected_item"]`
and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::parse_query`. It pulls out
a price (`under $30`), a size (`size M`, `size US 8.5`, `size W30`, or a size
after a comma at the end, like `tee, M`), and uses the rest as the
description. I used regex instead of the model because it's free, gives the
same answer every time, and when it gets something wrong I can see why in the
pattern. The downside is that it misses phrasing it doesn't know. A price
without a dollar sign (`under 30`, `under thirty dollars`) and a shoe size
without "US" (`size 8`) aren't picked up. Those words stay in the description
and that filter is skipped, with no warning.

**What moves through the session:** Each step writes its result into the
session, and the next step reads its input back out of it:

1. `query`: what the user typed.
2. `parsed`: the description, size and max price from `parse_query`.
3. `search_results`: the list `search_listings` returned.
4. `selected_item`: the first search result.
5. `outfit_suggestion`: what `suggest_outfit` returned for `selected_item`
   and `wardrobe`.
6. `fit_card`: what `create_fit_card` returned for `outfit_suggestion` and
   `selected_item`.

If the run stops early (an empty search, or the model can't be reached),
`error` gets a message and the fields after that point stay None.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ AI201_CACHE=0 python app.py ask 'vintage graphic tee under $30'
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1 Y2K Baby Tee — Butterfly Print Baggy straight-leg jeans, dark wash Vintage black denim jacket Chunky …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: scored this cute little butterfly print y2k baby tee on depop for just $18 and i am obsessed. it looks so good…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit 1
Y2K Baby Tee — Butterfly Print
Baggy straight-leg jeans, dark wash
Vintage black denim jacket
Chunky white sneakers
Black crossbody bag
This look balances the ultra-feminine butterfly graphic with chunky streetwear staples for a classic 2000s contrast.

Outfit 2
Y2K Baby Tee — Butterfly Print
Wide-leg khaki trousers
Brown leather belt
Black combat boots
The earthy tan trousers and rugged boots ground the pastel tee, leaning into a trendy mixed-aesthetic vibe.

  Fit card: scored this cute little butterfly print y2k baby tee on depop for just $18 and i am obsessed. it looks so good paired with baggy jeans and chunky sneakers for that classic 2000s contrast. honestly such a steal for the rotation.

2 model calls this session, 636 prompt + 165 output tokens
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Outfit 1:
- Vintage Levi's 501 Jeans — Medium Wash
- White ribbed tank top
- Vintage black denim jacket
- Chunky white sneakers
- Black crossbody bag

Why it works: This classic denim-on-denim pairing leans into the vintage streetwear vibe, while the fitted top balances the relaxed jeans and sneakers.

Outfit 2:
- Vintage Levi's 501 Jeans — Medium Wash
- Oversized grey crewneck sweatshirt
- Black combat boots
- Brown leather belt
- Black crossbody bag

Why it works: Tucking the medium wash denim into boots creates a grunge-inspired silhouette, contrasted by the cozy, oversized proportions of the grey crewneck.
```

```
$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage levis 501 jeans on depop for $38 and I am obsessed. The medium wash has that perfectly broken-in look without any of the work. Throwing them on with some fresh white sneakers for the ultimate effortlessly cool weekend fit.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* My instructor gave us helper code for
  `search_listings` (a stopword list, keyword matching and size matching). I
  gave it to Claude and asked where it went and how to build the tool around
  it.
- *What came back:* Claude ran the code before using it and found that it
  crashed on any search with a size. `p.strip().upper` was missing its `()`,
  so it raised an `AttributeError`. It also found two places where the code
  didn't match my Tool Inventory: "looking" and "size" weren't skipped as
  filler words, and `W30` didn't match `W30 L30`.
- *What I changed:* I had Claude fix the `.upper()` call and add "looking"
  and "size" to the stopword list. For `W30`, I chose to change my README
  instead of the code, because splitting sizes on spaces would have made
  `US 8` match `US 9`.

**Moment 2**

- *What I asked for:* I asked Claude to check my draft criteria: how it would
  test each one using only the sentence, whether two people would score it
  the same, and what would make it fail.
- *What came back:* It said criterion 5 (a model outage gives a message, not
  a traceback) could never fail through `app.py` or `run_eval.py`, because
  both already catch every error and hide the traceback. It also said
  criterion 4 compared 10 items, so it didn't fit the 5-try run log, and that
  the ids in criterion 3 don't show up in the trace.
- *What I changed:* I rewrote criterion 5 so it runs through `run_eval.py`
  with a broken API key and passes only if each try shows "stopped early"
  instead of "CRASHED" and the message names the key. I changed criterion 4
  to one query run 5 times, and criterion 3 to compare titles, which do show
  up in the trace.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

Both runs were made by `run_eval.py::main` with the cache off. Rows 1 to 4
come from `results/run_2026-10-18_2254_before.md`. Row 5 comes from
`results/run_2026-10-18_2258_outage.md`. For that run I took my key, changed
its last character, and passed it in as an environment variable for that one
command, so `.env` itself was never edited. Only row 5 of the outage run
counts.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The same item reaches every tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Repeat runs don't reuse an opening sentence | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. A model outage stops the run with a message instead of crashing | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Criterion 1**, try 1, from `results/run_2026-10-18_2254_before.md`. The
loop is `agent.py::run_agent`, and the fit card comes from
`tools.py::create_fit_card`.

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Scored this adorable butterfly print Y2K baby tee on Depop for just $18. I am obsessed with how it looks dressed down with baggy dark wash denim and a vintage jacket for that ultimate early 2000s street style vibe. Honestly might just live in this top all summer.
```

**Criterion 2**, try 1, from `results/run_2026-10-18_2254_before.md`. The
branch is in `agent.py::run_agent`, and the message comes from
`agent.py::_nothing_found_message`. The trace ends at the branch, with no
`suggest_outfit` step.

```
- stopped early: yes — Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
- selected_item: (none)
- search_results: 0

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
```

**Criterion 3**, try 1, from `results/run_2026-10-18_2254_before.md`. The
session is filled in by `agent.py::run_agent`. The same title shows up as the
first search result (step 2), as `selected_item`, and as the input to
`suggest_outfit` (step 4) and `create_fit_card` (step 5).

```
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1: - Y2K Baby Tee — Butterfly Print - Baggy straight-leg jeans, dark wash - Vintage black denim jacket …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Scored this little butterfly print Y2K baby tee on depop for just $18 and I am obsessed. It looks so good pair…
```

**Criterion 4**, all five tries, from `results/run_2026-10-18_2254_before.md`
(scenario "fit card openers don't repeat"). This criterion compares tries
with each other, so one try isn't enough to show it. The cards come from
`tools.py::create_fit_card`. No two share an opening sentence.

```
Try 1
scored this y2k butterfly print baby tee on depop for just $18 and i am obsessed. it looks so good paired with wide-leg trousers and combat boots for that perfect mix of sweet and edgy. definitely my new go-to top for throwing together a quick fit.

Try 2
scored this y2k butterfly baby tee on depop for $18 and it's honestly the cutest piece ever. obsessed with how it looks dressed down with baggy dark denim and chunky sneakers for that ultimate 2000s street style. total nostalgia trip in the best way possible.

Try 3
Found this adorable butterfly print y2k baby tee on depop for $18 and I am obsessed. I can already picture it with baggy denim and chunky sneakers for the ultimate retro look. It also looks so cute tucked into khaki trousers with combat boots for that grungy, mixed-style vibe.

Try 4
scored this Y2K baby tee with the cutest butterfly print on depop for just $18. it looks so good with baggy dark jeans and chunky sneakers for that total throwback look. can also dress it down with khakis and combat boots when i want a little edge.

Try 5
Found this absolute dream of a butterfly print baby tee on Depop and I am obsessed. For only $18, it brings the ultimate Y2K energy whether I am pairing it with baggy denim or toughening it up with combat boots. Honestly such a steal for my rotation.
```

**Criterion 5**, try 1, from `results/run_2026-10-18_2258_outage.md`. The
message comes from the `ModelUnavailable` handler in `agent.py::run_agent`,
and the "What the service said" part comes from `generate.py::_explain`.

```
- stopped early: yes — The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 10 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.
What the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] model unavailable
      →    stopping, search results kept
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

`python app.py ask 'vintage graphic tee under $30' --trace`. Step 2 is the
MCP call. The outfit and fit card came from the build cache (see the last
line), since I had run this query before.

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit One Pair the Y2K Baby Tee — Butterfly Print with the baggy straight-leg jeans, dark wash, vintage black…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: scored this little butterfly print y2k baby tee on depop for just $18 and i am obsessed. it looks so good tuck…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit One
Pair the Y2K Baby Tee — Butterfly Print with the baggy straight-leg jeans, dark wash, vintage black denim jacket, and chunky white sneakers. The fitted pink and purple butterfly graphic contrasts the dark indigo denim for a balanced streetwear look, while the chunky sneakers tie the Y2K vibe together.

Outfit Two
Pair the Y2K Baby Tee — Butterfly Print with the wide-leg khaki trousers, brown leather belt, and black combat boots. Tucking the pastel baby tee into the tan trousers grounds the pastel tones with earth colors, and the combat boots add an unexpected grunge edge to the cottagecore print.

  Fit card: scored this little butterfly print y2k baby tee on depop for just $18 and i am obsessed. it looks so good tucked into baggy dark denim for that effortless streetwear vibe. honestly might live in this all summer.

0 model calls this session, 2 served from cache
```

**Empty search**

`python app.py ask 'designer ballgown size XXS under $5' --trace`. It stops
at step 3, the branch, so it's two steps shorter than the happy path.

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

  Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.

0 model calls this session
```

**Failure modes, triggered on purpose**

I triggered each failure once to check that the agent says what broke and
what to try. None of them crashed, hung or went silent, so I didn't need to
add a handler.

1. **Empty search.** `python app.py ask 'designer ballgown size XXS under $5'`.
   No listing is a ballgown. The branch in `agent.py::run_agent` stopped
   after the search, so `suggest_outfit` never ran and no model calls were
   made. The message names each filter I set and how to loosen it:

   ```
     Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
   Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.

   0 model calls this session
   ```

2. **Empty wardrobe.**
   `python app.py ask 'vintage graphic tee under $30' --empty-wardrobe`.
   `tools.py::suggest_outfit` saw 0 wardrobe items and switched to a prompt
   that asks for general styling ideas. It gave two outfits made from
   clothes the user doesn't own yet, and the fit card still worked:

   ```
   (running with an empty wardrobe)
   [1] parse_query
         in:  vintage graphic tee under $30
         out: dict with keys: description, size, max_price
   [2] search_listings (via MCP)
         in:  dict with keys: description, size, max_price
         out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
         →    10 match(es)
   [3] select_item
         out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
   [4] suggest_outfit
         in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
         out: Outfit one: pair the baby tee with low-rise light-wash cargo pants and chunky white platform sneakers. This wo…
         →    0 wardrobe item(s)
   [5] create_fit_card
         in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
         out: Found this adorable butterfly print Y2K baby tee on depop for just $18. I am so obsessed with how it looks sty…

     Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

     Outfit:   Outfit one: pair the baby tee with low-rise light-wash cargo pants and chunky white platform sneakers. This works because the baggy utility bottoms balance the cropped, fitted top for an authentic early-2000s silhouette. 

   Outfit two: tuck the tee into a pink corduroy mini skirt and layer with knee-high white boots. This works because it leans into the sweet cottagecore crossover trend while keeping the color palette cohesive.

     Fit card: Found this adorable butterfly print Y2K baby tee on depop for just $18. I am so obsessed with how it looks styled with low-rise cargo pants and chunky sneakers for that ultimate early-2000s baggy-meets-fitted silhouette. It also looks insanely cute tucked into a pink corduroy mini skirt with knee-high boots.

   2 model calls this session, 351 prompt + 163 output tokens
   ```

3. **Model unavailable.** Instead of editing `.env`, I set a fake key for one
   command only, with the cache off so the model really gets called:
   `$env:GEMINI_API_KEY='not-a-real-key'; $env:AI201_CACHE='0'; python app.py ask 'black leather jacket under $60'`.
   This works because `config.py` loads `.env` without overriding variables
   that are already set. The service rejected the key on the first call in
   `suggest_outfit`. `generate.py` turned that into `ModelUnavailable`, and
   the handler in `agent.py::run_agent` caught it. There was no retry, no hang
   and no stack trace, and the search results were kept:

   ```
   [1] parse_query
         in:  black leather jacket under $60
         out: dict with keys: description, size, max_price
   [2] search_listings (via MCP)
         in:  dict with keys: description, size, max_price
         out: 10 items: Platform Mary Janes — Black Patent, Oversized Flannel Shirt — Plaid Red/Black, 90s Track Jacket — Navy/White Stripe … +7 more
         →    10 match(es)
   [3] select_item
         out: Platform Mary Janes — Black Patent ($55.0, depop)
   [4] model unavailable
         →    stopping, search results kept

     The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 10 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.
   What the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

   1 model calls this session
   ```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
