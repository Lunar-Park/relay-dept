// /api/contact — receives the contact form, forwards it as an email via Resend.
// Zero dependencies: uses the global fetch (Node 18+, Vercel default Node 20).
//
// Security: origin check + in-memory rate limit + Cloudflare Turnstile verify
// (see api/_lib.js). Honeypot field for cheap bot filtering.
//
// Required env vars (set in Vercel → Settings → Environment Variables):
//   RESEND_API_KEY       — your Resend API key (re_...)
//   RESEND_FROM_EMAIL    — verified sender, e.g. "Relay Dept <noreply@relaydept.com>"
//   CONTACT_TO_EMAIL     — where submissions land, e.g. "hello@relaydept.com"
//   TURNSTILE_SECRET_KEY — Cloudflare Turnstile secret (set for production!)
//   ALLOWED_ORIGIN       — comma-separated, e.g. "https://relaydept.com,https://www.relaydept.com"
//                          (defaults to https://relaydept.com; localhost always allowed)

const { json, checkOrigin, clientIp, createRateLimiter, verifyTurnstile } = require('./_lib');

const RESEND_URL = 'https://api.resend.com/emails';
// 5 contact submissions per IP per 10 minutes.
const limiter = createRateLimiter({ windowMs: 10 * 60 * 1000, max: 5 });
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

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

  // Honeypot: a real user never fills the hidden "_hp" field. Silently "succeed".
  if (body._hp) return json(res, 200, { ok: true });

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

  const name = String(body.name || '').trim();
  const email = String(body.email || '').trim();
  const project = String(body.project || '').trim();
  const message = String(body.message || '').trim();

  if (!name || !email) return json(res, 400, { ok: false, error: 'Name and email are required.' });
  if (!EMAIL_RE.test(email)) return json(res, 400, { ok: false, error: 'That email address looks invalid.' });
  if (name.length > 200 || email.length > 320 || project.length > 500 || message.length > 5000) {
    return json(res, 400, { ok: false, error: 'One of the fields is too long.' });
  }

  // Turnstile (network) — after cheap checks
  const ts = await verifyTurnstile(body.token, ip, process.env.TURNSTILE_SECRET_KEY);
  if (!ts.ok) return json(res, 403, { ok: false, error: 'Verification failed. Please reload and try again.' });

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error('RESEND_API_KEY is not set');
    return json(res, 500, { ok: false, error: 'Server not configured.' });
  }

  const from = process.env.RESEND_FROM_EMAIL || 'Relay Dept <noreply@relaydept.com>';
  const to = process.env.CONTACT_TO_EMAIL || 'hello@relaydept.com';

  const html = [
    `<div style="font-family:-apple-system,Inter,sans-serif;max-width:560px;margin:auto;color:#1A1A1A">`,
    `<p style="font-family:monospace;font-size:12px;letter-spacing:.1em;color:#C23B4A;margin:0 0 16px">// NEW INQUIRY — RELAYDEPT.COM</p>`,
    `<table style="width:100%;border-collapse:collapse;font-size:15px">`,
    `<tr><td style="padding:6px 0;color:#6B6B6B;width:90px;vertical-align:top">Name</td><td style="padding:6px 0"><strong>${escapeHtml(name)}</strong></td></tr>`,
    `<tr><td style="padding:6px 0;color:#6B6B6B;vertical-align:top">Email</td><td style="padding:6px 0"><a href="mailto:${escapeHtml(email)}" style="color:#C23B4A">${escapeHtml(email)}</a></td></tr>`,
    project ? `<tr><td style="padding:6px 0;color:#6B6B6B;vertical-align:top">Working on</td><td style="padding:6px 0">${escapeHtml(project)}</td></tr>` : '',
    message ? `<tr><td style="padding:6px 0;color:#6B6B6B;vertical-align:top">Message</td><td style="padding:6px 0;white-space:pre-wrap">${escapeHtml(message)}</td></tr>` : '',
    `</table>`,
    `<p style="font-family:monospace;font-size:11px;color:#9A9A9A;margin-top:24px">Reply directly to this email to respond.</p>`,
    `</div>`,
  ].join('');

  try {
    const r = await fetch(RESEND_URL, {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from,
        to,
        reply_to: `${name} <${email}>`,
        subject: `New inquiry from ${name}${project ? ' — ' + project.slice(0, 60) : ''}`,
        html,
      }),
    });

    if (!r.ok) {
      const detail = await r.text().catch(() => '');
      console.error('Resend error', r.status, detail);
      return json(res, 502, { ok: false, error: 'Email delivery failed. Please try again.' });
    }
    return json(res, 200, { ok: true });
  } catch (err) {
    console.error('contact handler error', err);
    return json(res, 500, { ok: false, error: 'Something went wrong. Please email us directly.' });
  }
};
