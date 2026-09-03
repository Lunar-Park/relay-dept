# Transcript → Content Pipeline

A Claude skill that turns one recording transcript into publish-ready content — **blog posts, social threads, show notes, and video summaries** — all in your brand's voice, in a single pass. Point it at a folder of brand docs once to build a reusable **brand profile**, then drop in a transcript and get channel-native content out, without fabricated facts or quotes. It also exports **editor-ready timecode files** (FCPXML for Resolve/FCP, FCP7 XML for Premiere markers, EDL for clip selects) so cutting the source recording is fast.

> **Status:** Concept / v1 (skill) · **Owner:** D + Claude

## What's Included

- **The skill** (`skill/SKILL.md`) — a self-contained Claude skill with the full workflow, quality bar, and messy-input handling
- **Brand identity ingestion** (`skill/references/brand-identity.md`) — point at a folder of brand docs; the skill builds a structured `brand-profile.md` that drives every output's voice, vocabulary, and formatting
- **4 format references** — tuned instructions for blog posts, social threads, show notes, and video summaries
- **Editor handoff** (`skill/references/timecode-export.md` + `skill/scripts/build_timecode.py`) — emits FCPXML (Resolve/FCP), FCP7 XML (Premiere markers), EDL (clip selects), and CSV from the segments used, with source timecodes carried into every content piece
- **Transcript cleaner** (`skill/scripts/clean_transcript.py`) — handles plain transcripts and `.vtt`/`.srt` captions; strips filler, normalizes speakers/diarization, dedupes rolling captions, preserves timestamps
- **Examples** (`examples/`) — a sample transcript, a sample `.vtt`, a content map, and a folder of brand docs to build a profile from

## Who It's For

Creators, podcasters, marketers, and teams who record a lot (interviews, webinars, calls, videos) and want to repurpose each recording into multiple content pieces — fast, and consistently in their own brand voice.

## How It Works

```
transcript-content-pipeline/
├── skill/
│   ├── SKILL.md                 # The skill: workflow + quality bar
│   ├── references/
│   │   ├── brand-identity.md    # Brand-docs ingestion + profile template
│   │   ├── blog-post.md         # Blog post format spec
│   │   ├── social-thread.md     # X / LinkedIn thread spec
│   │   ├── show-notes.md        # Podcast/video show notes spec
│   │   ├── video-summary.md     # Video summary / YT description spec
│   │   └── timecode-export.md   # Editor handoff: FCPXML / EDL / CSV
│   └── scripts/
│       ├── clean_transcript.py  # Pre-processing helper (txt + vtt/srt)
│       └── build_timecode.py    # Content map → FCPXML / EDL / CSV
├── examples/
│   ├── sample-transcript.txt    # Plain transcript to try it on
│   ├── sample-captions.vtt      # Caption file to test the cleaner
│   ├── sample-content-map.json  # Example content map for the exporter
│   └── brand-docs/              # Sample brand docs → build a profile from
├── package.sh                   # Build the uploadable skill zip
└── README.md

# At runtime the skill creates:
#   brand/brand-profile.md       # Generated brand profile (source of truth)
#   output/<recording-slug>/     # Content pieces + content-map.json + edit.fcpxml/.xml/.edl/.csv
```

## Install

Copy the `skill/` folder into your skills directory and rename it:

```bash
cp -r skill ~/.claude/skills/transcript-content-pipeline
```

Then in Claude Code (or claude.ai):

**1. Build your brand profile once:**

> "Use the transcript-content-pipeline skill to build our brand profile from `examples/brand-docs/`."

Claude reads the docs, infers your voice, and writes `brand/brand-profile.md`. Review and tweak it — it's the source of truth for every output.

**2. Then repurpose any recording:**

> "Turn this transcript into a blog post and an X thread."

Claude detects the skill, cleans the transcript, applies your brand profile, and generates each format against its reference spec — writing files to `output/`.

## Try It

```bash
# Preview the cleaner on a plain transcript
python skill/scripts/clean_transcript.py examples/sample-transcript.txt --stats

# ...and on a .vtt caption file (auto-detected)
python skill/scripts/clean_transcript.py examples/sample-captions.vtt --stats

# Build editor timecode files from a content map
python skill/scripts/build_timecode.py examples/sample-content-map.json --format all --out /tmp/edit
# -> /tmp/edit.fcpxml (Resolve/FCP), /tmp/edit.xml (Premiere markers),
#    /tmp/edit.edl (clip selects, both), /tmp/edit.csv
```

Then ask Claude: *"Build the brand profile from `examples/brand-docs/`, then use it to turn `examples/sample-transcript.txt` into show notes + a video summary, with editor timecode files."*

## Roadmap

- **v1 (now):** Claude skill — 4 content formats + brand profile + editor timecode export (FCPXML/EDL/CSV)
- **v2 (planned):** MCP server wrapping the same logic (`build_brand_profile`, `ingest_transcript`, `generate_blog`, `generate_thread`, `build_timecode`, …) so it works in any MCP client and can hit transcription APIs directly

The skill's reference files are the source of truth for each format — the future MCP server will reuse them rather than duplicating prompts.

---

*Built by [RelayDept](https://relaydept.com) — tools for people who build things.*
