# Reference: Brand Identity

Brand identity is the engine of this skill. Every content piece — blog, thread, show notes, video summary — must sound like it came from *one brand*, not from a generic AI. This file defines how to (a) ingest a folder of brand docs and (b) produce a structured **brand profile** that drives all downstream generation.

## The brand profile is the source of truth

Once a brand profile exists, every format reference (`blog-post.md`, `social-thread.md`, etc.) inherits from it. Voice, vocabulary, CTAs, and formatting conventions all come from the profile. If a format spec and the brand profile ever conflict, **the brand profile wins** (except for hard platform limits like X's character count).

The canonical location is `brand/brand-profile.md` inside the working project. Always check there first before asking the user anything about voice.

## Ingesting brand docs

When the user points to a folder of brand material (or there's no profile yet), build one:

1. **Discover.** Read every file in the brand folder. Common inputs:
   - Brand/style guides, tone-of-voice docs
   - Existing blog posts, newsletters, landing pages, social posts (best signal — real voice)
   - Mission/about pages, positioning docs, pitch decks
   - Glossaries, messaging frameworks, persona docs
   - Logos/visual assets — note them but this skill is about *written* identity
   - File types: `.md`, `.txt`, `.pdf`, `.docx`, `.html`. Extract text; for PDFs/HTML, pull the readable content.
2. **Extract signal, not boilerplate.** From real published examples, infer how the brand *actually* writes — sentence length, formality, humor, emoji use, capitalization habits, recurring phrases. Stated guidelines matter, but real samples matter more.
3. **Resolve conflicts.** If a style guide says "formal" but every real post is casual, trust the real posts and flag the discrepancy to the user.
4. **Fill the template** below. Where evidence is thin, mark the field `[NEEDS INPUT]` rather than guessing — then ask the user to confirm those specific fields.
5. **Write** the result to `brand/brand-profile.md` and show the user a short summary of what you inferred. Let them correct it before generating content.

If there are no brand docs at all, offer to build a minimal profile from a few questions (name, audience, 3 voice adjectives, examples of brands they admire).

## Brand profile template

Generate the profile in exactly this structure so it's reusable and machine-readable:

```markdown
---
brand: [Brand name]
updated: [DATE]
source_docs: [list of files ingested]
---

# Brand Profile: [Brand name]

## One-liner
[What the brand does, in one sentence, in the brand's own voice]

## Positioning & mission
[2-4 sentences: who they serve, the change they create, what makes them different]

## Audience
- Primary: [who]
- They care about: [pains/desires]
- Reading level / sophistication: [e.g. practitioner, exec, general]

## Voice
- **Three adjectives:** [e.g. direct, warm, irreverent]
- **We sound like:** [short description / a comparable brand or person]
- **We never sound like:** [anti-patterns]
- **Formality:** [1-5, where 1=very casual, 5=corporate]
- **Humor:** [none / dry / playful / meme-y]
- **Person & tense:** [e.g. first-person plural "we", present tense]

## Vocabulary
- **Use:** [preferred terms, product names with exact casing]
- **Avoid:** [banned words, jargon, competitor terms, clichés]
- **Spelling/casing rules:** [e.g. "RelayDept" one word, lowercase tweets, Oxford comma yes/no]

## Formatting conventions
- **Headlines:** [style — sentence case? Title Case? curiosity vs benefit?]
- **Emoji:** [never / sparingly / freely — and which ones]
- **Hashtags:** [count + placement per platform]
- **Links/CTAs:** [standard CTAs and where they go]
- **Punctuation quirks:** [em dashes, ellipses, exclamation policy]

## Boilerplate & assets
- **Standard CTA:** [text]
- **Bio/sign-off:** [text]
- **Standard links:** [site, newsletter, social — or PLACEHOLDER]

## Voice samples (in-brand)
> [2-3 short example sentences written in the brand voice, drawn from or modeled on real docs. These are the gold standard the model should match.]

## Open questions
- [Anything marked NEEDS INPUT for the user to confirm]
```

## Applying the profile during generation

When generating any content piece:
- Load `brand/brand-profile.md` first.
- Match the **voice samples** — they're the calibration target.
- Enforce the **Vocabulary** (use/avoid) and **Formatting conventions** as hard rules.
- Use the brand's **Standard CTA / sign-off** instead of inventing one.
- Keep faithfulness intact — brand voice changes *how* something is said, never *what facts* are claimed.

## Multiple brands

If the user works across brands, support `brand/<brand-slug>/brand-profile.md` and ask which brand a given run is for. Default to the only profile if there's just one.
