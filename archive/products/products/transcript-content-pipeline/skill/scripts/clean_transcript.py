#!/usr/bin/env python3
"""Clean a raw recording transcript for content generation.

Handles plain transcripts and caption files (.vtt/.srt): strips filler words,
collapses repeated whitespace, normalizes speaker/diarization labels, dedupes
rolling-caption artifacts, and preserves a timestamp per segment. Designed to
run before extracting/summarizing a transcript in the Transcript -> Content
Pipeline skill.

Usage:
    python clean_transcript.py input.vtt              # prints cleaned text
    python clean_transcript.py input.srt -o clean.txt # writes to file
    python clean_transcript.py input.txt --stats      # also print word counts
    python clean_transcript.py input.vtt --no-time    # drop timestamps
"""

import argparse
import re
import sys

# Filler words/phrases removed only when they stand alone (won't touch real words).
# Kept conservative: words like "right"/"actually"/"literally" often carry meaning,
# so we only strip unambiguous verbal-filler tokens and discourse phrases.
FILLERS = [
    "um", "uh", "erm", "hmm", "uhh", "umm",
    "you know", "i mean", "sort of", "kind of",
    "like i said", "okay so", "so yeah", "yeah so",
]

# Matches "Speaker:", "JOHN:", "Interviewer 1:" at the start of a line
SPEAKER_RE = re.compile(r"^\s*([A-Z][A-Za-z0-9 _'-]{0,30}):\s*")

# Diarization tags like [SPEAKER_00], (Speaker 1), <v John> (VTT voice spans)
DIARIZATION_RE = re.compile(
    r"[\[(<]\s*(?:v\s+)?speaker[ _-]?(\d+|[A-Za-z]+)\s*[\])>]",
    re.IGNORECASE,
)
VTT_VOICE_RE = re.compile(r"<v\s+([^>]+)>", re.IGNORECASE)

# SRT/VTT cue timing line, e.g. "00:00:01,000 --> 00:00:04,000"
CUE_TIMING_RE = re.compile(
    r"(\d{1,2}:\d{2}:\d{2})[.,]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[.,]\d{3}"
)
# A standalone integer line = SRT cue index
CUE_INDEX_RE = re.compile(r"^\d+$")
# Inline VTT tags like <00:00:01.000> and <c> styling
INLINE_TAG_RE = re.compile(r"<[^>]+>")


def is_caption_file(text: str) -> bool:
    return text.lstrip().startswith("WEBVTT") or bool(CUE_TIMING_RE.search(text))


def hhmmss_to_short(ts: str) -> str:
    """00:02:14 -> 02:14 ; 01:02:14 stays 01:02:14."""
    parts = ts.split(":")
    if len(parts) == 3 and parts[0] == "00":
        return f"{parts[1]}:{parts[2]}"
    return ts


def parse_captions(text: str):
    """Parse .vtt/.srt into [(timestamp_or_None, text), ...] segments."""
    segments = []
    cur_ts = None
    buf = []

    def flush():
        if buf:
            line = " ".join(buf).strip()
            # Convert VTT voice spans (<v Name>) to speaker labels BEFORE
            # stripping inline tags, or the speaker name is lost.
            line = VTT_VOICE_RE.sub(lambda m: f"{m.group(1).strip()}: ", line)
            line = INLINE_TAG_RE.sub("", line).strip()
            if line:
                segments.append((cur_ts, line))
        buf.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.upper().startswith("WEBVTT") or line.startswith("NOTE"):
            flush()
            continue
        m = CUE_TIMING_RE.search(line)
        if m:
            flush()
            cur_ts = hhmmss_to_short(m.group(1))
            continue
        if CUE_INDEX_RE.match(line):
            continue  # SRT cue number
        buf.append(line)
    flush()

    # Dedupe consecutive identical/overlapping lines (rolling-caption artifact)
    deduped = []
    for ts, line in segments:
        if deduped and (line == deduped[-1][1] or line in deduped[-1][1]):
            continue
        deduped.append((ts, line))
    return deduped


def normalize_diarization(line: str) -> str:
    line = DIARIZATION_RE.sub(lambda m: f"Speaker {m.group(1)}:", line)
    line = VTT_VOICE_RE.sub(lambda m: f"{m.group(1).strip()}: ", line)
    # Convert ">>" turn markers (common in broadcast captions) to a break
    line = re.sub(r"\s*>>\s*", "\n", line)
    return line


def remove_fillers(text: str) -> str:
    for f in FILLERS:
        pattern = re.compile(rf"\b{re.escape(f)}\b,?\s*", re.IGNORECASE)
        text = pattern.sub("", text)
    return tidy_punctuation(text)


def tidy_punctuation(text: str) -> str:
    """Clean up artifacts left behind after filler removal."""
    # Drop orphaned punctuation left at the start of a sentence/clause
    text = re.sub(r"(^|[.?!:]\s+)[,?.!]+\s*", r"\1", text)
    # Collapse doubled spaces and space-before-punctuation
    text = re.sub(r"\s+([,.?!])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    # Re-capitalize the first letter after sentence-ending punctuation
    text = re.sub(
        r"([.?!]\s+)([a-z])",
        lambda m: m.group(1) + m.group(2).upper(),
        text,
    )
    return text


def normalize_speakers(line: str) -> str:
    m = SPEAKER_RE.match(line)
    if not m:
        return line
    name = m.group(1).strip()
    rest = line[m.end():]
    if name.isupper():
        name = name.title()  # JOHN -> John
    return f"{name}: {rest}"


def clean_line(line: str) -> str:
    line = normalize_diarization(line)
    pieces = []
    for sub in line.split("\n"):
        sub = normalize_speakers(sub)
        sub = remove_fillers(sub)
        sub = re.sub(r"[ \t]{2,}", " ", sub).strip()
        if sub:
            pieces.append(sub)
    return "\n".join(pieces)


def clean(text: str, keep_time: bool = True) -> str:
    if is_caption_file(text):
        segments = parse_captions(text)
        lines = []
        for ts, line in segments:
            cleaned = clean_line(line)
            if not cleaned:
                continue
            if keep_time and ts:
                lines.append(f"({ts}) {cleaned}")
            else:
                lines.append(cleaned)
    else:
        lines = [c for c in (clean_line(l) for l in text.splitlines()) if c]

    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip() + "\n"


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean a transcript for content generation.")
    ap.add_argument("input", help="Path to the raw transcript (.txt/.md/.vtt/.srt)")
    ap.add_argument("-o", "--output", help="Write cleaned text here (default: stdout)")
    ap.add_argument("--stats", action="store_true", help="Print before/after word counts to stderr")
    ap.add_argument("--no-time", action="store_true", help="Drop timestamps from caption files")
    args = ap.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as e:
        print(f"error: could not read {args.input}: {e}", file=sys.stderr)
        return 1

    result = clean(raw, keep_time=not args.no_time)

    if args.stats:
        before, after = word_count(raw), word_count(result)
        pct = (1 - after / before) * 100 if before else 0
        kind = "caption file" if is_caption_file(raw) else "plain transcript"
        print(f"[{kind}] words: {before} -> {after} ({pct:.0f}% reduction)", file=sys.stderr)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(result)
        print(f"wrote cleaned transcript to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
