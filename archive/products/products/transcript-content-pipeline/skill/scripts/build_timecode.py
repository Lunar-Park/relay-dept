#!/usr/bin/env python3
"""Build editor-ready timecode files from a content map.

Takes a JSON "content map" of segments selected from a transcript (each with a
start time, optional end time, a name, and an optional note) and emits files you
can import into a video editor so the cut-down/editing process is fast:

  - FCPXML (.fcpxml)  -> DaVinci Resolve (native), Final Cut Pro
  - XMEML (.xml)      -> Premiere Pro (FCP7 XML), as sequence markers
  - EDL (.edl)        -> Premiere Pro and DaVinci Resolve (CMX3600), as clip selects
  - CSV (.csv)        -> spreadsheet / Resolve marker import / manual reference

Segments with BOTH start and end become ranges (clips in the EDL, ranged markers
in FCPXML). Segments with only a start become point markers.

Input JSON shape:
{
  "title": "Maya Chen Interview",
  "fps": 30,                       # 24, 23.976, 25, 29.97, 30, 60 ...
  "media": "interview.mov",        # optional source file name (reel/clip name)
  "segments": [
    {"start": "00:00", "end": "00:12", "name": "Cold open hook", "note": "blog intro"},
    {"start": "01:10", "name": "The 3-customer rule", "note": "thread post 3"}
  ]
}

Timecodes accept: "SS", "MM:SS", "HH:MM:SS", "HH:MM:SS:FF", or a number of seconds.

Usage:
  python build_timecode.py map.json --format all --out output/edit
  python build_timecode.py map.json --format edl > selects.edl
"""

import argparse
import json
import re
import sys
from xml.sax.saxutils import escape


# --- timecode helpers -------------------------------------------------------

def parse_seconds(value) -> float:
    """Parse a timecode string or number into seconds (float)."""
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s:
        raise ValueError("empty timecode")
    parts = s.split(":")
    try:
        nums = [float(p) for p in parts]
    except ValueError as e:
        raise ValueError(f"bad timecode {value!r}") from e
    if len(parts) == 1:                       # SS(.ms)
        return nums[0]
    if len(parts) == 2:                       # MM:SS
        return nums[0] * 60 + nums[1]
    if len(parts) == 3:                       # HH:MM:SS
        return nums[0] * 3600 + nums[1] * 60 + nums[2]
    if len(parts) == 4:                       # HH:MM:SS:FF  (frames handled by caller fps)
        return nums[0] * 3600 + nums[1] * 60 + nums[2]  # frames added in to_frames
    raise ValueError(f"bad timecode {value!r}")


def trailing_frames(value, fps: float) -> int:
    """Extract the :FF frame field from an HH:MM:SS:FF string, else 0."""
    s = str(value).strip()
    parts = s.split(":")
    if len(parts) == 4:
        return int(round(float(parts[3])))
    return 0


def to_frames(value, fps: float) -> int:
    return int(round(parse_seconds(value) * fps)) + trailing_frames(value, fps)


def frames_to_smpte(frames: int, fps: float) -> str:
    """Non-drop SMPTE timecode HH:MM:SS:FF."""
    f = int(round(fps))
    if f <= 0:
        f = 30
    hh = frames // (3600 * f)
    mm = (frames // (60 * f)) % 60
    ss = (frames // f) % 60
    ff = frames % f
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def frame_duration(fps: float) -> str:
    """FCPXML frameDuration rational for common rates."""
    table = {
        23.976: "1001/24000s",
        29.97: "1001/30000s",
        59.94: "1001/60000s",
    }
    key = round(fps, 3)
    if key in table:
        return table[key]
    return f"1/{int(round(fps))}s"


def timebase_ntsc(fps: float):
    """FCP7/xmeml (timebase, ntsc) pair for a frame rate."""
    table = {
        23.976: (24, "TRUE"),
        29.97: (30, "TRUE"),
        59.94: (60, "TRUE"),
    }
    key = round(fps, 3)
    if key in table:
        return table[key]
    return (int(round(fps)), "FALSE")


# --- normalization ----------------------------------------------------------

def normalize(data: dict):
    fps = float(data.get("fps", 30))
    title = data.get("title", "Untitled Edit")
    media = data.get("media") or "MEDIA"
    segs = []
    for i, raw in enumerate(data.get("segments", []), 1):
        if "start" not in raw:
            print(f"warning: segment {i} has no 'start', skipping", file=sys.stderr)
            continue
        start_f = to_frames(raw["start"], fps)
        end_f = to_frames(raw["end"], fps) if raw.get("end") not in (None, "") else None
        if end_f is not None and end_f <= start_f:
            end_f = start_f + 1  # guarantee at least one frame
        segs.append({
            "start_f": start_f,
            "end_f": end_f,
            "name": str(raw.get("name", f"Segment {i}")).strip(),
            "note": str(raw.get("note", "")).strip(),
            "is_range": end_f is not None,
        })
    segs.sort(key=lambda s: s["start_f"])
    return {"fps": fps, "title": title, "media": media, "segments": segs}


# --- exporters --------------------------------------------------------------

def build_fcpxml(m: dict) -> str:
    fps = m["fps"]
    fdur = frame_duration(fps)
    segs = m["segments"]
    total = max([s["end_f"] or s["start_f"] for s in segs], default=0) + int(round(fps))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!DOCTYPE fcpxml>",
        '<fcpxml version="1.10">',
        "  <resources>",
        f'    <format id="r1" name="FFVideoFormatRateUndefined" frameDuration="{fdur}" width="1920" height="1080"/>',
        "  </resources>",
        "  <library>",
        f'    <event name="{escape(m["title"])}">',
        f'      <project name="{escape(m["title"])}">',
        f'        <sequence format="r1" tcStart="0s" tcFormat="NDF">',
        "          <spine>",
        f'            <gap name="Timeline" offset="0s" start="0s" duration="{total}/{int(round(fps))}s">',
    ]
    for s in segs:
        start = f'{s["start_f"]}/{int(round(fps))}s'
        dur_f = (s["end_f"] - s["start_f"]) if s["is_range"] else 1
        dur = f'{dur_f}/{int(round(fps))}s'
        val = escape(s["name"])
        note = f' note="{escape(s["note"])}"' if s["note"] else ""
        lines.append(f'              <marker start="{start}" duration="{dur}" value="{val}"{note}/>')
    lines += [
        "            </gap>",
        "          </spine>",
        "        </sequence>",
        "      </project>",
        "    </event>",
        "  </library>",
        "</fcpxml>",
        "",
    ]
    return "\n".join(lines)


def build_xmeml(m: dict) -> str:
    """FCP7 'xmeml' XML — imports into Premiere Pro as sequence markers.

    Premiere reads the legacy Final Cut Pro 7 XML (root <xmeml>), not modern
    .fcpxml. Sequence-level <marker> elements come in as timeline markers; a
    range uses in/out frames, a point marker uses out=-1.
    """
    fps = m["fps"]
    tb, ntsc = timebase_ntsc(fps)
    segs = m["segments"]
    total = max([s["end_f"] or s["start_f"] for s in segs], default=0) + tb

    def rate_block(indent: str) -> str:
        return (
            f"{indent}<rate>\n"
            f"{indent}  <timebase>{tb}</timebase>\n"
            f"{indent}  <ntsc>{ntsc}</ntsc>\n"
            f"{indent}</rate>"
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!DOCTYPE xmeml>",
        '<xmeml version="4">',
        "  <sequence>",
        f"    <name>{escape(m['title'])}</name>",
        f"    <duration>{total}</duration>",
        rate_block("    "),
        "    <timecode>",
        rate_block("      "),
        "      <frame>0</frame>",
        "      <displayformat>NDF</displayformat>",
        "    </timecode>",
        "    <media>",
        "      <video>",
        "        <format>",
        "          <samplecharacteristics>",
        rate_block("            "),
        "            <width>1920</width>",
        "            <height>1080</height>",
        "          </samplecharacteristics>",
        "        </format>",
        "      </video>",
        "    </media>",
    ]
    for s in segs:
        out_f = s["end_f"] if s["is_range"] else -1
        lines += [
            "    <marker>",
            f"      <name>{escape(s['name'])}</name>",
            f"      <comment>{escape(s['note'])}</comment>",
            f"      <in>{s['start_f']}</in>",
            f"      <out>{out_f}</out>",
            "    </marker>",
        ]
    lines += ["  </sequence>", "</xmeml>", ""]
    return "\n".join(lines)


def build_edl(m: dict) -> str:
    fps = m["fps"]
    reel = "AX"
    out = [f"TITLE: {m['title']}", "FCM: NON-DROP FRAME", ""]
    rec = 0  # record-timeline playhead, in frames
    for i, s in enumerate(m["segments"], 1):
        src_in = s["start_f"]
        src_out = s["end_f"] if s["is_range"] else s["start_f"] + 1
        length = src_out - src_in
        rec_in, rec_out = rec, rec + length
        rec = rec_out
        out.append(
            f"{i:03d}  {reel:<8} V     C        "
            f"{frames_to_smpte(src_in, fps)} {frames_to_smpte(src_out, fps)} "
            f"{frames_to_smpte(rec_in, fps)} {frames_to_smpte(rec_out, fps)}"
        )
        out.append(f"* FROM CLIP NAME: {s['name']}")
        if s["note"]:
            out.append(f"* COMMENT: {s['note']}")
        out.append("")
    return "\n".join(out)


def build_csv(m: dict) -> str:
    fps = m["fps"]
    rows = ["Timecode In,Timecode Out,Type,Name,Note"]
    for s in m["segments"]:
        tc_in = frames_to_smpte(s["start_f"], fps)
        tc_out = frames_to_smpte(s["end_f"], fps) if s["is_range"] else ""
        kind = "range" if s["is_range"] else "marker"
        name = '"' + s["name"].replace('"', '""') + '"'
        note = '"' + s["note"].replace('"', '""') + '"'
        rows.append(f"{tc_in},{tc_out},{kind},{name},{note}")
    return "\n".join(rows) + "\n"


BUILDERS = {
    "fcpxml": (build_fcpxml, "fcpxml"),
    "xmeml": (build_xmeml, "xml"),
    "edl": (build_edl, "edl"),
    "csv": (build_csv, "csv"),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build editor timecode files from a content map.")
    ap.add_argument("input", help="Path to the content-map JSON")
    ap.add_argument("--format", choices=["fcpxml", "xmeml", "edl", "csv", "all"], default="all")
    ap.add_argument("--out", help="Output basename/dir (writes <out>.<ext>). Omit to print one format to stdout.")
    args = ap.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: could not read JSON {args.input}: {e}", file=sys.stderr)
        return 1

    m = normalize(data)
    if not m["segments"]:
        print("error: no usable segments in content map", file=sys.stderr)
        return 1

    formats = ["fcpxml", "xmeml", "edl", "csv"] if args.format == "all" else [args.format]

    if not args.out:
        if len(formats) > 1:
            print("error: choose a single --format when printing to stdout", file=sys.stderr)
            return 1
        builder, _ = BUILDERS[formats[0]]
        sys.stdout.write(builder(m))
        return 0

    base = args.out
    written = []
    for fmt in formats:
        builder, ext = BUILDERS[fmt]
        path = f"{base}.{ext}"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(builder(m))
        written.append(path)
    print("wrote: " + ", ".join(written), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
