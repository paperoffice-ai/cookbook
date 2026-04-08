#!/usr/bin/env node
/** PaperOffice AI — Webhooks (Subscribe + Receiver) */
import { createHmac, timingSafeEqual } from "node:crypto";
import { createServer } from "node:http";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Error: PAPEROFFICE_API_KEY not set");
  process.exit(1);
}

const headers = {
  Authorization: `Bearer ${api_key}`,
  "Content-Type": "application/json",
};
const webhook_secret = process.env.PAPEROFFICE_WEBHOOK_SECRET || "YOUR_WEBHOOK_SECRET";

async function subscribe_webhook(url, events) {
  const response = await fetch(`${api_base}/webhooks/subscribe`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      name: "my_first_webhook",
      url,
      events,
      secret: webhook_secret,
    }),
  });
  return response.json();
}

async function list_webhooks() {
  const response = await fetch(`${api_base}/webhooks/list`, {
    headers: { Authorization: `Bearer ${api_key}` },
  });
  return response.json();
}

async function test_webhook(subscription_id) {
  const response = await fetch(`${api_base}/webhooks/test`, {
    method: "POST",
    headers,
    body: JSON.stringify({ subscription_id }),
  });
  return response.json();
}

function verify_signature(payload, signature) {
  const expected = createHmac("sha256", webhook_secret)
    .update(payload)
    .digest("hex");
  try {
    return timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
  } catch {
    return false;
  }
}

// --- Register webhook and list all ---
const webhook_url = process.argv[2] || "https://example.com/webhook";

console.log(">>> Registering webhook...");
const sub_result = await subscribe_webhook(webhook_url, [
  "job.completed",
  "job.failed",
]);
console.log(sub_result);

const sub_data = sub_result.data || sub_result;
const sub_id = sub_data.subscription_id || sub_data.id || "";

console.log("\n>>> Listing webhooks...");
const webhooks = await list_webhooks();
console.log(`Total: ${webhooks.total ?? 0}`);
for (const sub of webhooks.subscriptions ?? []) {
  console.log(`  - ${sub.name}: ${sub.url}`);
}

if (sub_id) {
  console.log(`\n>>> Testing webhook (subscription_id=${sub_id})...`);
  const test_result = await test_webhook(sub_id);
  console.log(test_result);
}

// --- Express-like receiver (optionally with: node example.js serve) ---
if (process.argv[2] === "serve") {
  const server = createServer((req, res) => {
    if (req.method !== "POST" || req.url !== "/webhook") {
      res.writeHead(404);
      res.end();
      return;
    }

    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      const signature = req.headers["x-paperoffice-signature"] || "";
      if (!verify_signature(body, signature)) {
        res.writeHead(401, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Invalid signature" }));
        return;
      }

      const event = JSON.parse(body);
      console.log(`Webhook received: ${event.event}`);
      console.log(`  Job ID: ${event.job_id}`);
      console.log(`  Status: ${event.status}`);

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ received: true }));
    });
  });

  server.listen(5000, () => {
    console.log("\n>>> Webhook receiver running on http://localhost:5000/webhook");
  });
}
