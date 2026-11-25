# THE WORLD — Wednesday 25 November 2026

A one-page newspaper front page summing up the world news of
Wednesday 25 November 2026, from the morning wires of that day
(01:00–02:00 UTC and overnight into it).

## What it is

- **Masthead** — "THE WORLD — Wednesday 25 November 2026", 30 stories.
- **Three lead stories** — the CIA/ODNI breach; Houthis hitting
  Riyadh's tallest tower (11 wounded); Zelensky confirming Ukraine
  hit a Russian ship in the Gulf of Finland.
- **Numbered world map** — 12 places from today's news, with a
  legend naming each one, drawn by `render.py`.
- **Sections** — Europe (7 items), Middle East & Africa (5),
  Americas (6), Asia & Pacific (5), plus a Markets / Sport /
  Science strip (4). Every item carries a one-line summary and the
  source that reported it. 30 stories in total, across 7 regions
  and fields.
- **Footer** — a date-check line and a note to the picture editor.
  Events still to come are worded as such; nothing scheduled is
  presented as already happened.

No story is invented: every fact comes from a named source
(Reuters, AP, NYT, BBC, RFE/RL, Nextgov, CBS, Jagran Josh,
Disclosure News, Global Eye 24, Huddleworld), verified against
the morning's reporting of 25 November 2026.

## How to render

```
python3 render.py     # draws entry.png, 1024x1024, with Pillow
python3 main.py       # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` is Python 3.13 standard library only; it verifies the
copy is byte-identical (sha256) and is deterministic — run it
twice, same bytes.

## Files

- `render.py` — the front-page drawing program (Pillow + DejaVu)
- `main.py` — entry point (copies `entry.png` to the output directory)
- `entry.png` — the submitted image, exactly 1024x1024, under 1 MiB
