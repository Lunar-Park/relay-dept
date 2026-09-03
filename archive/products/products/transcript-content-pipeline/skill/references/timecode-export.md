# Reference: Timecode Export (editor handoff)

Goal: make editing the source recording effortless. Every content piece should be traceable back to *exactly where it came from* in the recording, and the user should be able to import a file straight into their editor to assemble the relevant clips.

This produces:
- **A content map** (`content-map.json`) — the structured list of source segments used
- **FCPXML** (`.fcpxml`) — import into **DaVinci Resolve** (native) or **Final Cut Pro**; markers
- **XMEML** (`.xml`, Final Cut Pro 7 XML) — import into **Premiere Pro** as **sequence markers**
- **EDL** (`.edl`, CMX3600) — import into **Premiere Pro** and **DaVinci Resolve** as **clip selects** (an assembly)
- **CSV** (`.csv`) — spreadsheet / Resolve marker import / manual reference

> Compatibility notes (verified against Adobe + Apple docs):
> - **Premiere Pro imports XML** — but the legacy **Final Cut Pro 7 `xmeml`** format (root `<xmeml>`, `.xml`), **not** modern `.fcpxml`. That's the file Premiere needs for markers (it's what Frame.io / marker-converter tools generate). Import via **File → Import** and pick the `.xml`; markers land on a sequence. To move them onto an existing timeline, paste them onto an adjustment layer.
> - **DaVinci Resolve** reads FCPXML (native) and EDL.
> - Use **xmeml** for Premiere *markers*, **EDL** for *assembling the selected clips* (works in both Premiere and Resolve). Generate all of them so the user is covered either way.

## Requirement: timecodes everywhere

Source timecodes are only available if the transcript has them. So:
- Prefer transcripts/captions **with timestamps** (the cleaner preserves them, including `.vtt`/`.srt`).
- If the transcript has **no timestamps**, tell the user the editor export can't be generated and offer to proceed with content only.

Every generated content piece must also carry inline source references so the editor (or the user) can find the moment — e.g. a pull quote tagged `[01:10]`, and a **Source timecodes** appendix at the bottom mapping each section/quote/post to its source time.

## Step 1 — Build the content map

As you select quotes and segments for the content pieces, record each one. Write `output/<recording-slug>/content-map.json`:

```json
{
  "title": "Maya Chen Interview",
  "fps": 30,
  "media": "maya-chen-interview.mov",
  "segments": [
    {"start": "00:18", "end": "00:34", "name": "Hook: features nobody asked for", "note": "blog intro + thread post 1"},
    {"start": "01:10", "end": "01:42", "name": "The 3-customer rule", "note": "thread post 3 + pull quote"},
    {"start": "01:48", "name": "Killed 40% of backlog (stat)", "note": "verify number on screen"}
  ]
}
```

Rules for the map:
- **`fps`** — ask the user, or default to 30 and say so. Frame rate must match the footage or timecodes drift. Common: 23.976, 24, 25, 29.97, 30, 60.
- **`media`** — the source filename if known; otherwise a placeholder (EDL/clip names will use it).
- **Ranges vs points:** include `end` for a usable clip (a "select"); omit `end` for a point marker (a moment to jump to). Use ranges where the transcript gives clear start/stop boundaries; use point markers for single moments or stats to verify on screen. ("Both" is expected and normal.)
- **`name`** — short, editor-facing label (shows as the clip/marker name).
- **`note`** — which content piece(s) it feeds, or an editing instruction.
- Timecodes accept `SS`, `MM:SS`, `HH:MM:SS`, `HH:MM:SS:FF`, or seconds.

## Step 2 — Generate the editor files

Run the script (do not hand-write FCPXML/EDL):

```bash
python scripts/build_timecode.py output/<slug>/content-map.json --format all --out output/<slug>/edit
# -> edit.fcpxml (Resolve/FCP), edit.xml (Premiere), edit.edl (both), edit.csv
```

Single format to stdout:
```bash
python scripts/build_timecode.py output/<slug>/content-map.json --format edl
```

## Step 3 — Tell the user how to import

In the manifest, include short import notes:
- **DaVinci Resolve:** File → Import → Timeline → import `edit.fcpxml` (markers) or `edit.edl` (clip selects; relink media). Lands on a timeline.
- **Premiere Pro — markers:** File → Import `edit.xml` (FCP7 XML). It creates a sequence with timeline markers. To get them onto your working timeline, paste them onto an adjustment layer.
- **Premiere Pro — selects:** File → Import `edit.edl` to build a sequence of the selected ranges; relink to the source media when prompted.
- Point markers (no end time) appear as zero/one-frame markers — trim out from there.

## Don't

- Don't invent timecodes. If the transcript lacks them, say so.
- Don't guess the frame rate silently — state the assumption.
- Don't hand-author FCPXML/EDL; always use `build_timecode.py` so the syntax stays valid.
