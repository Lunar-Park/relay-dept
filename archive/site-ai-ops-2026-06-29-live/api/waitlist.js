// /api/waitlist — adds an email to a Resend Audience for the given product.
// Zero dependencies: uses the global fetch (Node 18+, Vercel default Node 20).
//
// Security: origin check + in-memory rate limit + Cloudflare Turnstile verify
// (see api/_lib.js).
//
// Required env vars (set in Vercel → Settings → Environment Variables):
//   RESEND_API_KEY          — your Resend API key (re_...)
//   RESEND_AUDIENCE_CRATE   — audience id for the Crate waitlist
//   RESEND_AUDIENCE_ARRIVAL — audience id for the Arrival waitlist
//   TURNSTILE_SECRET_KEY    — Cloudflare Turnstile secret (set for production!)
//   ALLOWED_ORIGIN          — comma-separated origins (defaults to relaydept.com)

const { json, checkOrigin, clientIp, createRateLimiter, verifyTurnstile } = require('./_lib');

const RESEND_URL = 'https://api.resend.com/contacts';
// 5 waitlist signups per IP per 10 minutes.
const limiter = createRateLimiter({ windowMs: 10 * 60 * 1000, max: 5 });
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// product slug -> env var holding the audience id
const AUDIENCES = {
  crate: 'RESEND_AUDIENCE_CRATE',
  arrival: 'RESEND_AUDIENCE_ARRIVAL',
};

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return json(res, 405, { ok: false, error: 'Method not allowed' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { return json(res, 400, { ok: false, error: 'Invalid JSON' }); }
  }
  body = body || {};

  const product = String(body.product || '').trim().toLowerCase();
  const email = String(body.email || '').trim();

  if (!AUDIENCES[product]) return json(res, 400, { ok: false, error: 'Unknown product.' });

  // Origin guard
  const origin = checkOrigin(req, process.env.ALLOWED_ORIGIN || 'https://relaydept.com');
  if (!origin.ok) return json(res, 403, { ok: false, error: 'Submission not allowed from this origin.' });

  // Rate limit
  const ip = clientIp(req);
  const rl = limiter(ip);
  if (!rl.ok) {
    res.setHeader('Retry-After', String(Math.ceil((rl.retryAfterMs || 0) / 1000)));
    return json(res, 429, { ok: false, error: 'Too many submissions. Please try again later.' });
  }

  if (!email) return json(res, 400, { ok: false, error: 'Email is required.' });
  if (!EMAIL_RE.test(email)) return json(res, 400, { ok: false, error: 'That email address looks invalid.' });
  if (email.length > 320) return json(res, 400, { ok: false, error: 'Email is too long.' });

  // Turnstile (network) — after cheap checks
  const ts = await verifyTurnstile(body.token, ip, process.env.TURNSTILE_SECRET_KEY);
  if (!ts.ok) return json(res, 403, { ok: false, error: 'Verification failed. Please reload and try again.' });

  const apiKey = process.env.RESEND_API_KEY;
  const audienceId = process.env[AUDIENCES[product]];
  if (!apiKey || !audienceId) {
    console.error(`Missing env: ${!apiKey ? 'RESEND_API_KEY ' : ''}${!audienceId ? AUDIENCES[product] : ''}`);
    return json(res, 500, { ok: false, error: 'Server not configured.' });
  }

  try {
    const r = await fetch(RESEND_URL, {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, audienceId, unsubscribed: false }),
    });

    // Resend returns 409 if the contact already exists — treat as success.
    if (r.status === 409) return json(res, 200, { ok: true, already: true });
    if (!r.ok) {
      const detail = await r.text().catch(() => '');
      console.error('Resend contacts error', r.status, detail);
      return json(res, 502, { ok: false, error: 'Could not join the waitlist. Please try again.' });
    }
    return json(res, 200, { ok: true });
  } catch (err) {
    console.error('waitlist handler error', err);
    return json(res, 500, { ok: false, error: 'Something went wrong. Please try again.' });
  }
};
