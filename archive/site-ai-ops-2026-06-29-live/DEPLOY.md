# Relay Dept — Deploy Guide

Copy-paste-ready. Work top to bottom. Everything assumes the site deploys
from this `relaydept/` directory on Vercel.

---

## 1. Vercel — connect the site

1. **vercel.com → Add New → Project** → import `Lunar-Park/lunar-park-sites`.
2. **Configure Project:**
   - **Framework Preset:** `Other` (Vercel auto-detects; it's a static site + `/api` functions)
   - **Root Directory:** `relaydept`  ← important
   - **Build Command:** leave blank (no build step)
   - **Output Directory:** leave blank (Vercel serves the root)
   - **Install Command:** leave blank
3. **Deploy.** You'll get a `*.vercel.app` preview URL. The static pages,
   the `/api/contact` and `/api/waitlist` functions, `vercel.json` redirects,
   and security headers all deploy automatically. No further config needed
   for the site to *render* — only the forms/checkout need the secrets below.

> The `api/*.js` files use only the global `fetch` (Node 18+). Vercel's
> default Node 20 runtime handles them with zero dependencies — no
> `package.json` or `node_modules` required.

---

## 2. Enable Vercel Analytics

**Project → Analytics tab → Enable.** The script is already in every page's
`<head>` (`/_vercel/insights/script.js`). Enabling here turns it on. Free,
privacy-friendly, no cookie banner needed.

---

## 3. Resend — email + waitlists

The contact form mails you a notification; the waitlists add contacts to
Resend Audiences.

1. **resend.com → Sign up** (free tier: 3,000 emails/mo, 100 contacts).
2. **Verify your domain:** `relaydept.com`.
   Dashboard → Domains → Add → add the 3 DNS records (SPF / DKIM / DMARC)
   at your DNS provider → Verify. *Until this is done, you can only send
   to your own Resend account email — so do it first.*
3. **Get your API key:** Dashboard → API Keys → Create → `re_…`.
4. **Create two Audiences** (one per waitlist):
   - Dashboard → Audiences → Create → name it **`Crate Waitlist`** → copy the **Audience ID** (`a1b2c3…`)
   - Repeat → **`Arrival Waitlist`** → copy its **Audience ID**

---

## 4. Vercel — paste the secrets

**Project → Settings → Environment Variables.** Add each (Production +
Preview + Development as needed). Names must match exactly:

| Name | Value | Notes |
|------|-------|-------|
| `RESEND_API_KEY` | `re_…` | from step 3 |
| `RESEND_FROM_EMAIL` | `Relay Dept <noreply@relaydept.com>` | must be on the verified domain |
| `CONTACT_TO_EMAIL` | `hello@relaydept.com` | where contact-form mail lands |
| `RESEND_AUDIENCE_CRATE` | `a1b2c3…` | Crate Waitlist audience id |
| `RESEND_AUDIENCE_ARRIVAL` | `d4e5f6…` | Arrival Waitlist audience id |
| `TURNSTILE_SECRET_KEY` | `0x…` | Cloudflare Turnstile secret (see step 4a) — **REQUIRED for production** |
| `ALLOWED_ORIGIN` | `https://relaydept.com,https://www.relaydept.com` | form origin allowlist (defaults to apex; localhost always allowed) |

After adding: **Deployments → the latest → Redeploy** (env vars only apply
on a fresh build).

### 4a. Cloudflare Turnstile (form bot protection) — do this before launch

The forms ship with Cloudflare's **test keys** so the verification widget
renders and passes in preview. **Before going live you MUST swap in real
keys**, otherwise the forms have no real bot protection:

1. **dash.cloudflare.com → Turnstile → Add site** → hostname `relaydept.com`,
   widget mode **Managed** (invisible challenge — no puzzles for normal users).
2. Copy the two keys it gives you:
   - **Site Key** (`0x…`, public) → replace the test key in **3 files**:
     `index.html`, `crate.html`, `arrival.html` — search for `1x00000000000000000000AA`
     (it's in the `window.RELAY = { turnstileSiteKey: … }` line).
   - **Secret Key** (`0x…`, private) → set as the `TURNSTILE_SECRET_KEY` env var above.
3. Commit + redeploy.

A console warning (`verifying against the TEST secret`) fires on every form
submission until the secret is set — that's your reminder it's not live yet.

> **How the protection stacks:** Turnstile blocks ~95% of bots at the edge →
> an in-memory per-IP rate limit caps the rest at 5 submissions / 10 min →
> the origin check rejects off-site POSTs. (The rate limit is best-effort on
> serverless — per warm instance, resets on cold start — which is why
> Turnstile is the primary defense.)

### Test the forms
- Submit the **contact form** on `/` → check `CONTACT_TO_EMAIL`'s inbox.
- Submit the **Crate** waitlist → Audience **Crate Waitlist** gets a contact.
- Submit the **Arrival** waitlist → Audience **Arrival Waitlist** gets a contact.
- A repeat signup returns "You're already on the list" (handled: Resend 409 → success).

---

## 5. Stripe — Payment Links (Relay Pro, Paperclip)

1. **dashboard.stripe.com → Payment Links → Create.**
   - Product: `Relay Pro` — one-time **$299.00** → copy the link (`https://buy.stripe.com/…`)
   - Product: `Paperclip` — set your price → copy the link
2. **Paste into the code** (two spots each — search for `TODO(stripe)`):
   - `relay.html` → the `<a href="#" ... id="btn-relay">` → replace `#` with the Relay Pro link
   - `paperclip.html` → the `<a href="#" ... id="btn-paperclip">` → replace `#` with the Paperclip link
3. Commit + redeploy. Done — Stripe hosts the checkout; no webhook needed.

---

## 6. Custom domain

1. **Vercel → Project → Settings → Domains → Add** → `relaydept.com`.
2. Add `www.relaydept.com` too (Vercel auto-redirects it to the apex).
3. At your DNS/registrar, point:
   - `relaydept.com` → A record → `76.76.21.21` **(or use the nameservers Vercel shows you)**
   - Vercel will display the exact records on the Domains page — follow those.
4. Wait for DNS (minutes–hours). Vercel provisions the SSL cert automatically.

---

## 7. Post-launch SEO

- **Google Search Console** → add property `relaydept.com` → verify (DNS TXT) → submit `https://relaydept.com/sitemap.xml`.
- `robots.txt` and `sitemap.xml` are already in place and reference `https://relaydept.com`.

---

## File map (what's where)

```
relaydept/
├── index.html          # home (+ contact form → /api/contact)
├── blog.html           # post list
├── resources.html      # product grid
├── 404.html            # dark-themed not-found
├── relay.html          # product — Stripe Payment Link (TODO)
├── paperclip.html      # product — Stripe Payment Link (TODO)
├── crate.html          # product — waitlist → /api/waitlist
├── arrival.html        # product — waitlist → /api/waitlist
├── post.html           # slim redirect stub → /blog/*.html
├── blog/               # standalone posts (canonical) + .md sources
├── api/
│   ├── contact.js      # contact form → Resend email (origin + ratelimit + turnstile)
│   ├── waitlist.js     # waitlists → Resend Contacts/audiences (same guards)
│   └── _lib.js         # shared security helpers (NOT an endpoint — _-prefixed)
├── vercel.json         # redirects (/post.html?slug → /blog/slug.html) + headers
├── robots.txt
├── sitemap.xml
├── og-image.png        # 1200×630 social card
└── favicon.{svg,ico,png}
```

## Env-var quick reference (function → vars)

- **`/api/contact`** → `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `CONTACT_TO_EMAIL`, `TURNSTILE_SECRET_KEY`, `ALLOWED_ORIGIN`
- **`/api/waitlist`** → `RESEND_API_KEY`, `RESEND_AUDIENCE_CRATE`, `RESEND_AUDIENCE_ARRIVAL`, `TURNSTILE_SECRET_KEY`, `ALLOWED_ORIGIN`
