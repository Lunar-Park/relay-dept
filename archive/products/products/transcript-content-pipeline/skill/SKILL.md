---
name: transcript-content-pipeline
description: Turn a raw recording transcript (podcast, interview, webinar, sales call, YouTube video, meeting) into on-brand content pieces — blog posts, social threads, show notes, and video summaries — plus editor-ready timecode files (FCPXML for Resolve/FCP, FCP7 XML for Premiere markers, EDL for clip selects) so editing the source is fast. Ingests a folder of brand docs to build a reusable brand profile that keeps every output in the brand's voice. Use when the user provides a transcript (or a link/file path to one) and wants repurposed content, or asks to "turn this recording into a blog post / thread / show notes / summary", or asks to "set up / build our brand voice from these docs".
---

# Transcript → Content Pipeline

Take one recording transcript and produce condensed, publish-ready content in multiple formats — all in a consistent brand voice. The goal is to extract the *signal* from a long, messy, spoken-word transcript and reshape it for each channel, sounding like the brand wrote it, without inventing facts the speaker never said.

## When to use this skill

Trigger when the user:
- Pastes or points to a transcript and asks for content ("turn this into a blog post", "give me a thread", "write show notes")
- Asks to repurpose a recording, episode, interview, webinar, or talk
- Wants multiple content formats from one source
- Asks to **set up / build a brand voice or brand profile** from a folder of brand docs

## Core workflow

Follow these steps in order.

### Step 0 — Brand identity (HARD GATE — do this first, every time)

On-brand output is the whole point. **Do not generate any content until the brand profile is resolved.** This is a stop gate, not a suggestion — resolve it before Step 3 even if the user only handed you a transcript and asked for content.

Resolve it in this order:

1. **Check for an existing profile** at `brand/brand-profile.md` (or `brand/<brand-slug>/brand-profile.md`). If it exists, load it and continue.
2. **If none exists**, look for brand material — a `brand/` folder of source docs, or files the user attached. If you find any, follow `references/brand-identity.md` to ingest them, generate `brand/brand-profile.md`, show the user a summary, and let them correct it before generating content.
3. **If you find no profile and no brand docs, STOP and ask the user** — do not silently generate in a generic voice. Say something like: *"Before I write anything, I want it to sound like your brand. Point me to a folder of brand docs (style guide, a few published posts, your about page) and I'll build a brand profile — or answer 3 quick questions: who's your audience, three words for your voice, and a brand whose writing you admire?"* Only proceed in a generic voice if the user **explicitly** says they don't care about brand consistency.

The brand profile is the source of truth for voice, vocabulary, formatting, and CTAs across every format. **See `references/brand-identity.md`.**

This step can also run on its own — if the user just wants to "build our brand voice", do Step 0 and stop.

### Step 1 — Ingest & understand the transcript

1. Locate the transcript. It may be pasted inline, a file path, or a URL. If it's a file, read it. If it's a URL to a page, fetch and extract it.
2. Run `scripts/clean_transcript.py` to strip filler, normalize speaker labels, convert caption formats (`.vtt`/`.srt`), and preserve timestamps. Recommended for anything over ~2,000 words or any auto-generated/caption input.
3. Read the cleaned transcript fully before writing anything. Build a mental model of:
   - **Core thesis** — the one main point or story
   - **Key segments** — 3-7 distinct topics or beats
   - **Quotable lines** — verbatim phrases worth pulling
   - **Speakers** — who said what (for interviews/panels)
   - **Timestamps** — **capture the source timecode of every segment and quote you might use.** These carry through into the content pieces and the editor export. If the transcript has no timestamps, note that the timecode export won't be available.

### Step 2 — Confirm scope

Ask the user (only if not already specified):
- Which output formats they want (blog post / social thread / show notes / video summary — or all)
- Target platform for threads (X/Twitter vs LinkedIn — they differ in length and tone)
- Length target, if they have one
- Which brand the run is for, if multiple profiles exist

Don't re-ask about voice/tone — that comes from the brand profile. If the user already said "all formats" or gave clear direction, skip the questions and proceed.

### Step 3 — Generate each requested format

For each format, load the matching reference file **and** apply the brand profile (profile wins on any conflict except hard platform limits):

| Format | Reference file |
|--------|---------------|
| Blog post | `references/blog-post.md` |
| Social thread | `references/social-thread.md` |
| Show notes | `references/show-notes.md` |
| Video summary | `references/video-summary.md` |
| Timecode export (editor handoff) | `references/timecode-export.md` |

Generate formats in the order the user requested them.

**Carry source timecodes through.** As you pull a quote or build a section from a moment, tag it with its source timecode (e.g. a pull quote followed by `[01:10]`), and end each piece with a short **Source timecodes** appendix mapping content → original time. This makes editing trivial.

### Step 3.5 — Editor handoff (timecode export)

Unless the user opts out, build the editor files so cutting the recording is fast. As you select segments, record them in `output/<slug>/content-map.json`, then run `scripts/build_timecode.py` to emit **FCPXML** (Resolve/FCP markers), **XMEML** (`.xml`, FCP7 XML — Premiere markers), **EDL** (Premiere/Resolve clip selects), and **CSV**. Ask for the frame rate (default 30, and say so). **See `references/timecode-export.md`.** Skip only if the transcript has no timestamps (say so) or the user declines.

### Step 4 — Review pass

Before delivering, self-check every piece against the **Quality bar** below *and* the brand profile's voice samples, vocabulary, and formatting rules. Fix issues silently, then deliver.

## Output handling

- **Default location:** write outputs to `output/<recording-slug>/`, one file per format, e.g. `output/maya-chen-interview/blog-post.md`, `.../x-thread.md`, `.../show-notes.md`, `.../video-summary.md`. The editor handoff adds `content-map.json`, `edit.fcpxml`, `edit.xml`, `edit.edl`, and `edit.csv` in the same folder. Derive `<recording-slug>` from the recording topic/guest.
- **Bundle option:** if the user prefers a single document, write all formats into one `output/<recording-slug>/content-pack.md` with H1 sections per format.
- **Inline option:** if the user is just experimenting or asks to "show me", print to chat instead of writing files. When in doubt for a quick request, show inline; for a full multi-format run, write files.
- **Never overwrite silently:** if a target file exists, append a short numeric suffix or ask.
- **Always end with a manifest:** list the files written (paths) and any `[PLACEHOLDER]`s the user must fill (links, dates, titles, guest bio).

## Quality bar

Every output must pass these checks:

1. **On-brand** — Matches the brand profile's voice samples, vocabulary (use/avoid), and formatting conventions. Uses the brand's standard CTA/sign-off, not an invented one.
2. **Faithful** — Every claim, stat, and quote traces back to the transcript. Never fabricate facts, numbers, names, or quotes. If you paraphrase, keep the meaning intact. Mark direct quotes as quotes. Brand voice changes *how* something is said, never *what* is claimed.
3. **Condensed, not just trimmed** — Reshape the ideas; don't copy-paste sentences. A good blog post reads like it was written, not transcribed.
4. **Channel-native** — A thread sounds like a thread; show notes scan like show notes.
5. **Self-contained** — The reader shouldn't need the original recording to follow the piece.
6. **Hook-first** — Lead with the most interesting idea, not throat-clearing.
7. **No hallucinated metadata** — Don't invent episode numbers, dates, guest titles, or links. Use placeholders like `[GUEST TITLE]` and surface them in the manifest.
8. **Timecode-traceable** — Every pulled quote and key section carries its source timecode (inline + a Source timecodes appendix), and the editor export reflects the same moments. Never invent timecodes; if the transcript lacks them, say so.

## Handling messy input

- **No speaker labels / unclear who's talking** — Infer from context where safe; otherwise write neutrally and flag ambiguity to the user.
- **Auto-generated captions (`.vtt`/`.srt`, no punctuation)** — The cleaner converts these and strips cue numbers; re-segment into sentences before extracting.
- **Diarization tags** (`[SPEAKER_00]`, `>>`, etc.) — The cleaner normalizes these to speaker labels.
- **Very long transcripts (>10k words)** — Segment by topic first, summarize each segment, then compose the final pieces from the segment summaries.
- **Multiple recordings** — Ask whether to produce one combined piece or one per recording.

## Tips for great output

- Pull 2-4 verbatim quotes per piece — they add authenticity and are great for social.
- For threads, the first post is 80% of the value. Spend the most effort there.
- For blog posts, add descriptive H2/H3 headers so the piece is skimmable.
- For show notes, timestamps are the killer feature — preserve and format them.
- Always offer a short list of suggested titles/headlines; let the user pick.

## Extending later (MCP)

This skill is intentionally structured so the same logic can be exposed as an MCP server later (tools like `build_brand_profile`, `ingest_transcript`, `generate_blog`, `generate_thread`). The reference files — especially `brand-identity.md` — are the source of truth; an MCP implementation should reuse them rather than duplicating the prompts.
