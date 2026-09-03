# Relay Dept brand tokens

Source of truth is the live site (`archive/site-ai-ops-2026-06-29-live/index.html` `:root`), translated to paper in `Lunar-Park-KB/relay/brand/document-brand.md`.

| Token | Value | Role |
|---|---|---|
| `--rd-paper` | `#F2EEE8` | Content pages. Warm, from the site's type colour |
| `--rd-cover` | `#0D0D0D` | Cover page of client-facing documents only; site ground |
| `--rd-ink` | `#0D0D0D` | Body, headings |
| `--rd-ink-2` | `#5A5854` | Eyebrows, captions, footers, status strip |
| `--rd-ink-3` | `#8A8680` | Placeholders, "to be sourced" |
| `--rd-rule` | `#CFC9C1` | Hairlines: table rows, section dividers, strip borders |
| `--rd-band` | `#E8E4DF` | Table header fill where used; site type colour |
| `--rd-red` | `#C23B4A` | The bracket, the section square, the INTERNAL dot, the gate corner. One per page region |
| `--rd-red-dark` | `#8A2B36` | Links, signature lines |

Type: Space Grotesk 600 for headings and the wordmark; Inter 400/500 for body; JetBrains Mono 400/500 for the status strip, labels, table heads, footer. All three are on Google Fonts; the paper stylesheet imports them. Embed local files before Binder renders offline.

Wordmark: `RELAY[_] DEPT` in Space Grotesk 600 caps tracked 0.08em, the `[_]` in JetBrains Mono red at 70% size raised. The 3×3 red square from the favicon is the section marker.

Never: dark content pages, the 64px grid on content pages, lime, Limitless orange, LLC claims before formation.
