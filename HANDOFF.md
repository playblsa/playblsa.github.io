# BLSA End of Year Tournament — Project Handoff

## Context
12-team softball tournament (Barrhaven Ladies Softball Association), 2 pools of 6
(A1–A6, B1–B6), Sept 25–27, Manotick, Ontario. Started as a review of a proposed
schedule spreadsheet; grew into three planned deliverables — a master schedule
poster (PDF), individual team schedule cards (PDF), and a live schedule website
(single-file HTML).

**Current status: the poster PDF has been dropped** (not needed) — only the team
cards PDF and the website are still active.

**Goal for this handoff:** continue in Claude Code so it can work directly in the
local repo at `/Users/caseydoyle/src/blsa` (I — chat Claude — only have a sandboxed
environment, not access to that machine, so getting files there has been manual
copy/paste up to now).

## Repo state
- User created a GitHub repo, local clone at `/Users/caseydoyle/src/blsa`.
- Site should be pushed as `index.html` at the repo root — GitHub Pages needs that
  exact filename to auto-serve it. Enable via Settings → Pages → deploy from main
  branch, root folder.
- **Not yet confirmed live** — last step was handing the user `index.html` to
  manually commit/push; unconfirmed whether that's done yet.

## Architecture (single source of truth pattern)
Two Python data files feed both build scripts, so editing one place regenerates
everything consistently:

- **`schedule_data.py`** — `TEAM_NAMES` (code → display name), `TOURNAMENT_NAME`,
  `SLOTS` (the full day-by-day schedule: each slot has an `id`, `day`, `start`,
  `end`, `kind` [`game`/`lunch`/`buffer`/`playoff`], `d1`/`d2` team pairs,
  `score1`/`score2` [which team scorekeeps each diamond], `beer` [team on beer-tent
  duty], and **`result1`/`result2`** [`[runs_team_a, runs_team_b]` once final, else
  `None`] for game slots), `DAY_INFO`, plus helper functions `team_display()`,
  `team_pool()`, `team_games()`.
- **`menu_rules_data.py`** — food truck menu (Foodie LU), drinks & snacks price
  list, and the full tournament rules text (transcribed from the official rules
  PDF), structured as sections for both the PDF and website to consume.
- **`build_team_cards_pdf.py`** — generates the 15-page team cards PDF (12 personal
  team cards + shared Food Truck / Drinks & Snacks / Rules reference pages at the
  end, not duplicated per team).
- **`build_html.py`** — generates `interactive_schedule.html` (the live site).
  Self-contained, no external dependencies, no backend — pure static file.
- **`build_master_pdf.py`** — poster generator, currently unused/deprioritized but
  left intact in case it's wanted again later.

Regenerating after any data change is just: edit `schedule_data.py` (or
`menu_rules_data.py`), then `python3 build_html.py` and/or
`python3 build_team_cards_pdf.py`.

## Design system — "Lapis velvet evening"
Matched from a palette image the user provided. Same tokens used in both the PDF
(reportlab `HexColor`) and the website (CSS variables), just different names:

| Role | Hex | PDF constant | CSS var |
|---|---|---|---|
| Header/hero bg | `#081849` | `NAVY_DARK` | `--hero` |
| Page/card bg + light text-on-dark | `#ECDFD2` | `CREAM` | `--cream` |
| Diamond 1 + Scorekeeping badge | `#213885` | `LAPIS` | `--lapis` |
| Diamond 2 | `#5F3475` | `PLUM` | `--plum` |
| Beer tent badge / accent | `#893172` | `MAGENTA` | `--accent` |
| Secondary/muted text | `#7A7482` | `MUTED` | `--muted` |
| Borders | `#CCCACC` | `LINE` | `--line` |
| Main text ink | `#081849` | `INK` | `--ink` |
| Muted text on dark bg | `#C7BFC9` | `DARK_MUTED` | `--dark-muted` |

Important nuance: the old palette's gold was *light* (worked with dark text on
top); the new magenta accent is *dark*, so anywhere a badge/text sits on it needs
*light* (cream) lettering, not dark ink — this tripped us up once already, worth
remembering if extending the palette further.

Fonts: Helvetica-Bold/Helvetica/Courier-Bold in the PDF; system font stack
(`-apple-system` etc.) on the web, mono for times to match the PDF's "scoreboard"
feel.

## Final team names / pool assignments
Applied from final regular-season standings, straight rank order split into two
pools (confirmed by user):

- **Pool A:** A1 Bat-titudes, A2 Stealers, A3 Renegades, A4 Ice Cold Pitches,
  A5 Angels, A6 Big D's
- **Pool B:** B1 Rookies, B2 Swingers, B3 Metro Scrappers, B4 Dynamite Dames,
  B5 Basic Pitches, B6 The Misfits

## Notable bugs found & fixed along the way
1. **Incomplete/unbalanced round robin** in the originally-proposed schedule —
   each team should play 4 of 5 possible pool opponents; Pool B was uneven (one
   team had 3 games, another had 5) until a swap fixed it.
2. **Scorekeeping vs. beer-tent duty conflict** — same team assigned both in the
   same slot; resolved once user clarified only 2 players are needed to
   scorekeep, so the rest of the crew covers beer tent simultaneously (not a
   real conflict) — but a code bug then silently dropped the beer-tent entry
   whenever it coincided with a scorekeeping entry for 9 of 12 teams (a
   "pick one role" priority bug in both the PDF and website's per-team lookup).
   Fixed by allowing multiple duty entries per team per slot.
3. A `reportlab` `Frame.addFromList` quirk silently dropped rules text that
   didn't fit a column instead of properly returning the overflow — replaced
   with manual paragraph-height tracking across columns/pages.

## Score-results feature (just added, untested with real data)
- Each `game`-kind slot has `result1`/`result2` fields — set to
  `[runs_for_first_team_in_pair, runs_for_second_team_in_pair]` (matching the
  order of that diamond's `d1`/`d2` tuple) once a game is final; `None` until
  then.
- Each slot has a stable `id` (e.g. `FRI1`, `SAT2`, `SUN-POOLB`) for easy
  reference — though in practice the user has been telling chat-Claude scores
  in plain language ("Friday 6:15 game, Bat-titudes beat Big D's 8-3") rather
  than using IDs directly.
- **Playoff slots** (`SUN-POOLB`, `SUN-POOLA`) don't have known teams yet — they're
  just labels until finalists are determined Sunday. Data model has placeholder
  `teams`/`result` keys on those slots but nothing renders from them yet; this
  would need extending once playoff matchups are known.
- Website display: master view shows `"Bat-titudes 8 – 3 Big D's"` with a
  `FINAL` tag and the winning team's name/score highlighted (`.winner` class);
  each team's personal view shows a `WIN`/`LOSS`/`TIE` tag instead. Tested by
  temporarily injecting fake result data into a copy of the built HTML and
  confirming correct rendering via jsdom — production file currently has all
  results still `None` (never been fed a real score yet).
- Team cards PDF does **not** currently show results (static print artifact,
  wasn't in scope for live scores — flag if that's wanted too).

## What Claude Code should probably do next
1. Get these files into `/Users/caseydoyle/src/blsa` (this zip has everything).
2. Confirm `index.html` is committed/pushed and GitHub Pages is actually live;
   sanity-check the real URL.
3. Be ready to take score updates directly (in plain language is fine) during
   the tournament weekend, update the right slot's `result1`/`result2` in
   `schedule_data.py`, regenerate `index.html` via `build_html.py`, and
   commit/push directly — this was the main reason for moving to Claude Code,
   since it can touch the local repo/git directly instead of round-tripping
   files through chat.
