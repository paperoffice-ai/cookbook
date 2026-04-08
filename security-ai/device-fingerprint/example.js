#!/usr/bin/env node
/** PaperOffice AI — Verify device fingerprint */

const API_URL = "https://api.paperoffice.ai/latest/fingerprint/verify";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function verify_fingerprint(visitor_id, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ visitorId: visitor_id });
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const vid = process.argv[2] || "test_visitor_abc123";
const data = await verify_fingerprint(vid);

console.log(`Visitor ID:  ${data.visitorId}`);
console.log(`Verified:    ${data.verified}`);
console.log(`Reason:      ${data.reason}`);
console.log(`Status:      ${data.status}`);
