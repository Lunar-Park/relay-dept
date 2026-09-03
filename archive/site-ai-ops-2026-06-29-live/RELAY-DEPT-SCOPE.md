# Relay Dept — Build Scope

_Created: 2026-06-23_
_Priority: Content & functionality NOW → UI polish PHASE 2_
_Repo: github.com/Lunar-Park/lunar-park-sites (private)_
_Local: ~/lunar-park/lunar-park-sites/relaydept/_

---

## Phase 1: Content & Functionality

### 1.1 Home Page — Copy Refinement

**File:** `index.html`

Current copy is placeholder. Tighten it. Keep the tone: confident, understated, slightly ominous. Not corporate. Not salesy.

#### Hero
- **Headline (current):** "Relay builds agentic systems customized to your needs"
- **Direction:** Keep it short, one line. Examples of tone: "We build systems that think for you" / "Relay builds autonomous infrastructure" / "Your operations, automated"
- **Sub (current):** "We design autonomous AI infrastructure — agents that remember, coordinate, and execute without hand-holding."
- **Direction:** One sentence, max 60 words. What Relay does, not how.

#### What We Do (3 cards)
Current: Agent Systems, AI Infrastructure, Workflow Automation
- Each card: title (2-4 words) + description (1-2 sentences, max 25 words per sentence)
- Tone: matter-of-fact, no jargon, slightly ominous
- Example for Agent Systems: "Custom autonomous agents built around your workflows. Not chatbots — intelligent systems that handle real work across every platform you use."

#### How We Work (4 steps)
Current: Discovery, Design, Deploy, Evolve
- Each step: title (1-2 words) + description (1-2 sentences, max 20 words per sentence)
- Keep it tight. Don't over-explain.

#### Contact
- **Headline:** "Let's build something real"
- **Sub:** "Tell us what you're working on. We'll figure out if AI operations can give you the edge."
- Form fields: Name, Email, What are you working on?, Message (optional)
- Submit button: "Send →"
- Form action: `mailto:hello@relaydept.com` (no backend needed)

#### Nav
- Links: Services (#services), Process (#process), Blog (blog.html), Resources (resources.html)
- No CTA button in nav (keep it clean)

#### Footer
- Left: "© 2026 Relay Dept"
- Right: Blog, Resources, Twitter (links)

---

### 1.2 Blog Page — SEO Content Engine

**File:** `blog.html`
**New file:** `post.html` (blog post template)

This is the primary content driver. Blog posts build SEO authority and support the TikTok → website funnel.

#### Blog List Page (`blog.html`)
- Header: "Writing on AI, agents, and building systems"
- Post list format (current layout is good):
  - Date (YYYY-MM-DD format, left column)
  - Title + excerpt (middle column)
  - Tag (right column, burgundy color)
- Tags: AI Ops, Agents, Infrastructure, Strategy, Tutorial, Case Study
- 4-6 placeholder posts with realistic titles and excerpts (current placeholders are fine as starting point)

#### Blog Post Template (`post.html`)
Create a new file for individual blog posts. Structure:
- Post header: date, tag, title
- Post body: markdown-rendered or HTML content
- Estimated read time
- Back to blog link
- Share buttons (Twitter, LinkedIn — just link to intent URLs)
- Related posts section (2-3 posts, can be placeholder)

Post URL structure: `post.html?slug=why-most-ai-implementations-fail` or use hash-based routing

#### First Real Posts to Write
Write 2-3 actual blog posts. Suggested topics:
1. "What Is AI Operations?" — foundational, SEO-targeted, explains what Relay does
2. "Why Most AI Implementations Fail" — authority-building, problem-aware content
3. "Building Agents That Remember" — technical depth, shows expertise

Each post: 800-1500 words, conversational tone, no fluff. Include at least one heading, one list or bullet point section.

#### SEO per Post
- Title tag: "{Post Title} | Relay Dept"
- Meta description: 150 chars max, includes target keyword
- OG tags: title, description, image (can use a default relay-og.png for now)
- H1: post title
- Structured data: Article schema (nice to have, not blocking)

---

### 1.3 Resources Page — Products & Credibility

**File:** `resources.html`

Each resource = credibility signal + potential revenue/user acquisition.

#### Product Cards (2x2 grid, current layout is good)
Update the 4 placeholder cards with real info:

1. **Relay Agent Framework**
   - Status: Active
   - Description: Open-source framework for building persistent, multi-platform AI agents with memory, scheduling, and sub-agent orchestration.
   - CTA: "View on GitHub →" → link to repo (or placeholder #)
   - Link: https://github.com/Lunar-Park (placeholder)

2. **Paperclip**
   - Status: Active
   - Description: Lightweight agent monitoring dashboard. Real-time visibility into agent activity, tool usage, and system health.
   - CTA: "Documentation →" → link to docs (or placeholder #)

3. **Crate**
   - Status: In Development
   - Description: Visual catalog for creative assets. AI-assisted tagging, perceptual hashing, and curation tools for teams managing large media libraries.
   - CTA: "Coming soon →" → # or waitlist email

4. **Arrival**
   - Status: In Development
   - Description: Presence and state legibility for AI systems. Monitor what your agents are doing, where they are, and what they're paying attention to.
   - CTA: "Coming soon →" → # or waitlist email

#### SEO
- Title tag: "Resources | Relay Dept"
- Meta description: "Tools and systems built by Relay. Open-source AI agent framework, monitoring dashboard, and more."
- OG tags

---

### 1.4 Technical / Functionality

#### Deployment
- **Decide:** GitHub Pages vs Vercel (D is already paying for Vercel, but GitHub Pages is simpler)
- **Recommendation:** GitHub Pages for now (free, simple, matches the repo). Migrate to Vercel later if needed.
- If GitHub Pages: enable in repo settings, site lives at `lunar-park.github.io/lunar-park-sites/relaydept/`
- If Vercel: connect repo, set root directory to `relaydept/`

#### DNS (when ready)
- Point `relaydept.com` to deployed URL
- Add `www.relaydept.com` redirect if needed

#### Favicon
- Create a simple favicon: burgundy "R" on cream background, or just the Relay mark
- Format: `.ico` + `.png` (for different devices)
- Add to all pages: `<link rel="icon" type="image/x-icon" href="favicon.ico">`

#### SEO (all pages)
- Add to every page `<head>`:
  ```html
  <meta property="og:title" content="Page Title | Relay Dept">
  <meta property="og:description" content="Page description">
  <meta property="og:image" content="https://relaydept.com/og-image.png">
  <meta property="og:url" content="https://relaydept.com/page">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  ```
- Create a default `og-image.png` (1200x630, cream bg, Relay logo/text)

#### 404 Page
- Create `404.html`
- Simple: "Page not found" + link back to home
- Same nav/footer as other pages

#### Sitemap
- Create `sitemap.xml` listing all pages:
  - index.html
  - blog.html
  - resources.html
  - post.html (if using query params, list with ?slug= variants)
  - 404.html

#### Cross-links
- Add relaydept.com link in dspury.com footer or about section
- Add dspury.com link in relaydept.com footer

---

## Phase 2: UI Rewrite

After content is live, rewrite the visual layer. Don't touch content — just CSS and minimal HTML structure changes.

### Design Direction
- **Background:** Cream (#F5F0EB)
- **Text:** Charcoal (#1A1A1A) for headings, (#2C2C2C) for body, (#6B6B6B) for muted
- **Accent:** Burgundy (#6B1D2A) — used sparingly for emphasis
- **Fonts:** Space Grotesk (headings), Inter (body), SF Mono or JetBrains Mono (accents/code)
- **Brutalist elements:** ASCII art dividers, monospace labels, raw structural feel
- **Vibe:** Hermes Agent meets IBM Design Language. Clean but with edge.

### Specific UI Tasks
1. **Hero:** Add an ASCII art or geometric accent element (not just text). Consider a subtle grid pattern or border treatment.
2. **Section dividers:** Replace plain `border-bottom` with brutalist break rules (gradient lines, ASCII characters like `─────` or `▸▸▸`)
3. **Service cards:** Add a monospace number prefix, refine hover state (border animation or subtle shift)
4. **How We Work:** Consider a vertical timeline layout instead of 2x2 grid
5. **Contact form:** Minimal, brutalist input styling (bottom border only, no background)
6. **Nav:** Add a monospace accent or typewriter element for the brand name
7. **Footer:** Clean, minimal, monospace copyright
8. **Mobile:** Full responsive pass — test at 375px, 768px, 1024px, 1440px
9. **Micro-interactions:** Hover states, focus states, scroll-triggered reveals
10. **Background texture:** Optional subtle noise or grid pattern (CSS only, no images)

### What NOT to Touch in Phase 2
- Don't change any copy/text content
- Don't add new pages
- Don't change the page structure (sections stay the same)
- Don't remove functionality (forms, links, etc.)

---

## Phase 3: SEO & Growth (Post-Launch)

- [ ] Google Search Console — verify domain, submit sitemap
- [ ] Analytics — Plausible (privacy-friendly) or Umami
- [ ] Blog content calendar — aim for 1-2 posts per week
- [ ] Internal linking — link between blog posts where relevant
- [ ] TikTok funnel — mention relaydept.com in TikTok bio and video descriptions
- [ ] Backlink strategy — guest posts, mentions, directories
