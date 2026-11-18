# Run log — capstone_after

- Produced by: `run_eval.py::main`
- Loop: `agent.py::run_agent` · tools: `tools.py`
- Provider: scripted Gemini HTTP responses through the SDK
- Search: direct local tool (the shared trace still labels it 'via MCP')
- CLI output: `app.py::_ask_one`
- Structured records: `capstone_run_2026-11-17_225215_381467_capstone_after.jsonl`
- Tries per scenario: 3, caching off
- Temperature: 0.9
- When: 2026-11-17 22:53

Paste the table below into your README. Fill in the Criterion and
Target columns from `criteria.md`, then mark each try PASS or FAIL
from the output underneath and count them for the Verdict.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Verdict |
|---|---|---|---|---|---|
| 1. stalled outfit response |  |   |   |   |  |
| 2. outfit rate limit recovers |  |   |   |   |  |
| 3. outfit stays rate limited |  |   |   |   |  |
| 4. blank outfit response |  |   |   |   |  |
| 5. fit card fails after the outfit succeeds |  |   |   |   |  |

> The Try and Verdict columns are blank on purpose. Whether a try
> passed depends on the criterion you wrote, so it's yours to decide.
> Count the passes, then read that count against your target: a row
> targeting 4 of 5 with three PASS cells is MISSED (3/5).

---

## What actually happened

Real output, as text. Paste the relevant parts into your README —
the rubric asks for output, not a description of it.

### stalled outfit response

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- Trial elapsed: 8.984000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 0
- outfit elapsed: 6.562000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. The model request timed out. Try again.
```

- stopped early: yes — Outfit unavailable. The model request timed out. Try again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

**Try 2**

- Trial elapsed: 8.672000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 0
- outfit elapsed: 6.375000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. The model request timed out. Try again.
```

- stopped early: yes — Outfit unavailable. The model request timed out. Try again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

**Try 3**

- Trial elapsed: 8.843000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 0
- outfit elapsed: 6.375000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. The model request timed out. Try again.
```

- stopped early: yes — Outfit unavailable. The model request timed out. Try again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

### outfit rate limit recovers

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- Trial elapsed: 2.610000 s
- outfit HTTP attempts: 2
- fit_card HTTP attempts: 1
- outfit elapsed: 0.468000 s
- fit_card elapsed: 0.000000 s

CLI stdout

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
      out: Pair the tee with straight-leg jeans and white sneakers.
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the tee with straight-leg jeans and white sneakers.

  Fit card: Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.
```

CLI stderr

```
  [rate limit] retrying in 0.1s (attempt 2 of 3).
```

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Pair the tee with straight-leg jeans and white sneakers.
```

Fit card:

```
Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.
```

**Try 2**

- Trial elapsed: 2.359000 s
- outfit HTTP attempts: 2
- fit_card HTTP attempts: 1
- outfit elapsed: 0.500000 s
- fit_card elapsed: 0.000000 s

CLI stdout

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
      out: Pair the tee with straight-leg jeans and white sneakers.
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the tee with straight-leg jeans and white sneakers.

  Fit card: Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.
```

CLI stderr

```
  [rate limit] retrying in 0.1s (attempt 2 of 3).
```

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Pair the tee with straight-leg jeans and white sneakers.
```

Fit card:

```
Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.
```

**Try 3**

- Trial elapsed: 2.516000 s
- outfit HTTP attempts: 2
- fit_card HTTP attempts: 1
- outfit elapsed: 0.500000 s
- fit_card elapsed: 0.000000 s

CLI stdout

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
      out: Pair the tee with straight-leg jeans and white sneakers.
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the tee with straight-leg jeans and white sneakers.

  Fit card: Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.
```

CLI stderr

```
  [rate limit] retrying in 0.1s (attempt 2 of 3).
```

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Pair the tee with straight-leg jeans and white sneakers.
```

Fit card:

```
Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop.
```

### outfit stays rate limited

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- Trial elapsed: 2.547000 s
- outfit HTTP attempts: 3
- fit_card HTTP attempts: 0
- outfit elapsed: 0.579000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. Still rate limited after 3 attempts. Wait at least 1 second before trying again.
```

CLI stderr

```
  [rate limit] retrying in 0.1s (attempt 2 of 3).
  [rate limit] retrying in 0.1s (attempt 3 of 3).
```

- stopped early: yes — Outfit unavailable. Still rate limited after 3 attempts. Wait at least 1 second before trying again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

**Try 2**

- Trial elapsed: 2.500000 s
- outfit HTTP attempts: 3
- fit_card HTTP attempts: 0
- outfit elapsed: 0.578000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. Still rate limited after 3 attempts. Wait at least 1 second before trying again.
```

CLI stderr

```
  [rate limit] retrying in 0.1s (attempt 2 of 3).
  [rate limit] retrying in 0.1s (attempt 3 of 3).
```

- stopped early: yes — Outfit unavailable. Still rate limited after 3 attempts. Wait at least 1 second before trying again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

**Try 3**

- Trial elapsed: 2.688000 s
- outfit HTTP attempts: 3
- fit_card HTTP attempts: 0
- outfit elapsed: 0.578000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. Still rate limited after 3 attempts. Wait at least 1 second before trying again.
```

CLI stderr

```
  [rate limit] retrying in 0.1s (attempt 2 of 3).
  [rate limit] retrying in 0.1s (attempt 3 of 3).
```

- stopped early: yes — Outfit unavailable. Still rate limited after 3 attempts. Wait at least 1 second before trying again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

### blank outfit response

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- Trial elapsed: 2.562000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 0
- outfit elapsed: 0.375000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. The model returned no text. Try running the same search again.
```

- stopped early: yes — Outfit unavailable. The model returned no text. Try running the same search again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

**Try 2**

- Trial elapsed: 2.328000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 0
- outfit elapsed: 0.375000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. The model returned no text. Try running the same search again.
```

- stopped early: yes — Outfit unavailable. The model returned no text. Try running the same search again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

**Try 3**

- Trial elapsed: 2.250000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 0
- outfit elapsed: 0.375000 s

CLI stdout

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
[4] model unavailable
      →    stopping at outfit, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit unavailable. The model returned no text. Try running the same search again.
```

- stopped early: yes — Outfit unavailable. The model returned no text. Try running the same search again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

### fit card fails after the outfit succeeds

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- Trial elapsed: 2.218000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 1
- outfit elapsed: 0.375000 s
- fit_card elapsed: 0.000000 s

CLI stdout

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
      out: Pair the tee with straight-leg jeans and white sneakers.
      →    10 wardrobe item(s)
[5] model unavailable
      →    stopping at fit_card, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the tee with straight-leg jeans and white sneakers.

  Fit card unavailable. The model request failed (HTTP 400). Try again.
```

- stopped early: yes — Fit card unavailable. The model request failed (HTTP 400). Try again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Pair the tee with straight-leg jeans and white sneakers.
```

**Try 2**

- Trial elapsed: 2.313000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 1
- outfit elapsed: 0.391000 s
- fit_card elapsed: 0.000000 s

CLI stdout

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
      out: Pair the tee with straight-leg jeans and white sneakers.
      →    10 wardrobe item(s)
[5] model unavailable
      →    stopping at fit_card, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the tee with straight-leg jeans and white sneakers.

  Fit card unavailable. The model request failed (HTTP 400). Try again.
```

- stopped early: yes — Fit card unavailable. The model request failed (HTTP 400). Try again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Pair the tee with straight-leg jeans and white sneakers.
```

**Try 3**

- Trial elapsed: 2.203000 s
- outfit HTTP attempts: 1
- fit_card HTTP attempts: 1
- outfit elapsed: 0.375000 s
- fit_card elapsed: 0.000000 s

CLI stdout

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
      out: Pair the tee with straight-leg jeans and white sneakers.
      →    10 wardrobe item(s)
[5] model unavailable
      →    stopping at fit_card, earlier results kept

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the tee with straight-leg jeans and white sneakers.

  Fit card unavailable. The model request failed (HTTP 400). Try again.
```

- stopped early: yes — Fit card unavailable. The model request failed (HTTP 400). Try again.
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Pair the tee with straight-leg jeans and white sneakers.
```
