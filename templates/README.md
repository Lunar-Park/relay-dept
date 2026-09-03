# Templates

**Prose templates** (what to write) live in the KB: `Lunar-Park-KB/relay/productions/templates/`.

**Print templates** (how it looks) live in `print/`. `relay-paper.css` is the stylesheet; each `*.html` is a filled example of one document type that doubles as the template. Render with Chromium:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --print-to-pdf=out.pdf --no-pdf-header-footer print/production-treatment.html
```

Fonts come from Google Fonts for now; embed local files before anything renders offline in Binder.

Done: `production-treatment.html` (single page), `estimate.html` (dark cover, flowing pages, money tables; figures are examples from the superseded LA model). To do: SOW, capability sheet, delivery record, call sheet.

Multi-page documents use a fixed status strip and footer that Chromium repeats on every page, and a `.cover` section that paints over them. Page numbers cannot be set from CSS in Chromium; Binder adds them through its header and footer templates.
