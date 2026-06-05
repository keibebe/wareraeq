/**
 * WarEra API Proxy — Cloudflare Worker
 *
 * Forwards requests to api2.warera.io / gateway.warerastats.io,
 * adding the required Origin header and returning CORS headers
 * so your GitHub Pages site can call it from the browser.
 *
 * Free tier: 100,000 requests/day — plenty for personal use.
 */

const UPSTREAM = "https://gateway.warerastats.io/trpc/";
const FALLBACK = "https://api2.warera.io";

// Only allow your own GitHub Pages domain (and localhost for dev).
// Add or change this to match YOUR actual Pages URL.
const ALLOWED_ORIGINS = [
  "https://keibebe.github.io",   // ← change this
  "http://localhost",
  "http://127.0.0.1",
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    // CORS pre-flight
    if (request.method === "OPTIONS") {
      return corsResponse(null, 204, origin);
    }

    // Block requests from unknown origins
    const allowed = ALLOWED_ORIGINS.some(
      (o) => origin === o || origin.startsWith(o)
    );
    if (!allowed && origin !== "") {
      return corsResponse(JSON.stringify({ error: "Origin not allowed" }), 403, origin);
    }

    // Build the upstream URL — preserve path + query string
    const url = new URL(request.url);
    const upstreamURL = UPSTREAM + url.pathname + url.search;

    // Forward the request
    const upstreamHeaders = new Headers(request.headers);
    upstreamHeaders.set("Origin", "https://app.warera.io");
    upstreamHeaders.delete("Host"); // let fetch set the correct host

    let res;
    try {
      res = await fetch(upstreamURL, {
        method: request.method,
        headers: upstreamHeaders,
        body: request.method !== "GET" && request.method !== "HEAD"
          ? request.body
          : undefined,
      });
    } catch (_) {
      // Try fallback endpoint
      try {
        const fallbackURL = FALLBACK + url.pathname + url.search;
        res = await fetch(fallbackURL, {
          method: request.method,
          headers: upstreamHeaders,
          body: request.method !== "GET" && request.method !== "HEAD"
            ? request.body
            : undefined,
        });
      } catch (err) {
        return corsResponse(JSON.stringify({ error: err.message }), 502, origin);
      }
    }

    // Stream the response back with CORS headers added
    const body = await res.text();
    return corsResponse(body, res.status, origin, res.headers.get("Content-Type") || "application/json");
  },
};

function corsResponse(body, status, origin, contentType = "application/json") {
  const headers = {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-API-Key",
    "Access-Control-Max-Age": "86400",
    "Content-Type": contentType,
  };
  return new Response(body, { status, headers });
}
