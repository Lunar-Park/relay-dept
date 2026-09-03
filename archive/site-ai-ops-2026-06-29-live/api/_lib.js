// Shared security helpers for the relaydept API functions.
// Files/folders prefixed with "_" in /api are NOT deployed as endpoints
// by Vercel — safe to use as a local helper module.

// Cloudflare's always-pass test secret. Used as a fallback ONLY so preview
// works before TURNSTILE_SECRET_KEY is set. In production you MUST set the
// real secret (see DEPLOY.md) — a warning is logged when this fallback is used.
const TURNSTILE_TEST_SECRET = '1x0000000000000000000000000000000AA';

function json(res, status, body) {
  res.setHeader('Content-Type', 'application/json');
  return res.status(status).json(body);
}

// ─── Origin check ───
// Same-origin browser fetches send an Origin header we can validate.
// localhost/127.0.0.1 always allowed for local dev; production origins
// come from the ALLOWED_ORIGIN env var (comma-separated).
const LOCAL_ORIGIN = /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/;

function checkOrigin(req, allowedEnv) {
  const allowed = String(allowedEnv || '')
    .split(',')
    .map((s) => s.trim().replace(/\/$/, ''))
    .filter(Boolean);
  const origin = req.headers.origin || req.headers.referer || '';
  if (!origin) return { ok: false, reason: 'missing_origin' };
  if (LOCAL_ORIGIN.test(origin)) return { ok: true };
  try {
    const u = new URL(origin);
    const base = u.protocol + '//' + u.host;
    if (allowed.includes(base)) return { ok: true };
  } catch {
    /* malformed */
  }
  return { ok: false, reason: 'bad_origin' };
}

// ─── Client IP ───
function clientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  if (xff) return String(xff).split(',')[0].trim();
  return (req.socket && req.socket.remoteAddress) || 'unknown';
}

// ─── Rate limiter (in-memory, best-effort, per-instance) ───
// On Vercel serverless this state lives only on warm instances and resets
// on cold start — it is NOT a hard distributed limit. Turnstile is the
// primary abuse defense; this caps casual burst spam from a single IP.
function createRateLimiter({ windowMs, max }) {
  const hits = new Map();
  return function check(ip) {
    const now = Date.now();
    // prune expired entries so the map can't grow unbounded
    for (const [k, v] of hits) {
      if (now - v.windowStart > windowMs) hits.delete(k);
    }
    const rec = hits.get(ip);
    if (!rec || now - rec.windowStart > windowMs) {
      hits.set(ip, { windowStart: now, count: 1 });
      return { ok: true, remaining: max - 1 };
    }
    rec.count += 1;
    if (rec.count > max) {
      return { ok: false, retryAfterMs: windowMs - (now - rec.windowStart) };
    }
    return { ok: true, remaining: max - rec.count };
  };
}

// ─── Turnstile verification ───
async function verifyTurnstile(token, ip, envSecret) {
  if (!token) return { ok: false, reason: 'missing_token' };
  const secret = envSecret || TURNSTILE_TEST_SECRET;
  if (!envSecret) {
    console.warn(
      '[relaydept] TURNSTILE_SECRET_KEY not set — verifying against the TEST secret. Set it for production.'
    );
  }
  try {
    const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ secret, response: token, remoteip: ip }),
    });
    const data = await r.json();
    return { ok: !!data.success, reason: (data['error-codes'] || []).join(', ') || 'verification_failed' };
  } catch (err) {
    console.error('[relaydept] Turnstile verify error', err);
    return { ok: false, reason: 'verify_error' };
  }
}

module.exports = { json, checkOrigin, clientIp, createRateLimiter, verifyTurnstile };
