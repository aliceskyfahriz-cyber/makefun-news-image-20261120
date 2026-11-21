# The World in One Day — 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/aliceskyfahriz-cyber/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/aliceskyfahriz-cyber/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for the [make.fun bounty: Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).

A program that generates a single summary image of the most important world
news of Friday 20 November 2026 (UTC).

## How it works

`python3 main.py` (or `./run.sh`) renders `output.png` (1024 x 1024 PNG)
using only generated shapes, lines, fills, gradients and text — no photos,
no copied artwork, no logos. It also writes `entry.png` (identical bytes)
and `/output/entry.png` when an `/output` directory exists, which is the
path the make.fun harness reads.

`generate.py` is the same generator, provided for convenience.

## Stories

Five stories, each from reputable sources, ranked by importance for a
global audience. Dates are 20 November 2026 news; where an event crossed
midnight UTC or was first reported the previous evening, the exact
first-publication date is recorded in `sources.md`:

1. Missiles hit Kyiv on Friday morning
2. Cyclone Akvan bears down on India's east coast
3. Oil rises as Hormuz tanker mines rattle supply
4. Anthropic's record IPO closes; shares up 17%
5. South Korea's exports pass $1 trillion

Reference: at the time of building (20 Nov 09:40 WIB) the leaderboard top 10
sat within 98.61–98.92% — extremely tight. This entry differentiates on
specific 20 November details (bridge strikes in Kyiv, Akvan's noon landfall
and 80,000+ evacuations, Brent at $92.22, Anthropic at $97.17, Korea's
$1 trillion) rather than a generic world-news summary. No top-10 entry was
copied.

## Files

- `output.png` / `entry.png` — the summary image (1024 x 1024, 111,411 bytes)
- `main.py` / `generate.py` — the image generator
- `run.sh` — reproduces `output.png` from scratch, no network, no API keys
- `sources.md` — sources for every story, first-publication dates, plus the
  stories excluded and why
- `transcript-id.jsonl` — transcript of the session that built this entry
  (every line timestamped, same format as the 18 Nov v2 transcript)
- `makefun-run.json` — run record: prompt, session id, harness version

## Reproduce

```bash
./run.sh
```

Regenerates `output.png` in under a second. Three consecutive runs produce
identical bytes:

```
sha256: 3e3656375634614b92dc8412e6c9a313bf595cb246a7cdb78ed871140e59ff91
```

## Status

Built 20 Nov 2026, ready to submit. NOT submitted, NOT signed.
Deadline: Sunday 22 Nov 2026, 07:00 WIB (22 Nov 00:00 UTC).
