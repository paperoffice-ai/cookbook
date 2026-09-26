#!/usr/bin/env node
/** PaperOffice AI — GDPR-compliant anonymization of documents
 *
 * Template: document_anonymize | Param: file (not file_1!)
 * Categories: all, names, addresses, phone, email, iban, tax_id
 */
import { readFileSync, writeFileSync } from "node:fs";
import { basename } from "node:path";

/** HTTP 202 means the job is still running: follow job/get until it is completed. */
async function wait_for_result(data, token, api_base = "https://api.paperoffice.ai/latest", timeout_ms = 180000) {
  if (data.result || !data.job_id) return data;
  const deadline = Date.now() + timeout_ms;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 2000));
    const poll = await (await fetch(`${api_base}/job/get/${data.job_id}`, { headers: { Authorization: `Bearer ${token}` } })).json();
    if (poll.job_status === "completed" || poll.result || poll.job_result) {
      if (!poll.result && poll.job_result) poll.result = poll.job_result; // same payload, different key
      return poll;
    }
    if (poll.job_status === "failed" || poll.job_status === "error" || poll.status === "error") {
      throw new Error(`job failed: ${poll.message}`);
    }
  }
  throw new Error(`job ${data.job_id} not finished after ${timeout_ms / 1000}s`);
}

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Error: PAPEROFFICE_API_KEY not set");
  process.exit(1);
}

const input_file = process.argv[2];
const redact_categories = process.argv[3] ?? "all";

if (!input_file) {
  console.error("Usage: node example.js <document.pdf> [categories]");
  process.exit(1);
}

console.log(`→ Anonymizing: ${input_file} (categories: ${redact_categories})`);

const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file", new Blob([file_buffer]), basename(input_file));
form_data.append("template", "document_anonymize");
form_data.append("redact_categories", redact_categories);
form_data.append("processing_lane", "instant");

const response = await fetch(`${api_base}/job/add/workflow`, {
  method: "POST",
  headers: { Authorization: `Bearer ${api_key}` },
  body: form_data,
});

const data = await wait_for_result(await response.json(), api_key);
console.log(`Status: ${data?.status}`);

if (data?.status !== "success") {
  console.error("Error:", JSON.stringify(data, null, 2));
  process.exit(1);
}

const result = data?.result ?? {};
const download_urls = result.anonymized_pdf ?? result.files ?? [];
if (download_urls.length === 0) {
  console.error("Error: No download URL received");
  process.exit(1);
}

const pii = result.detected_pii;
if (pii?.audit_trail) {
  console.log(`Redacted entities: ${pii.audit_trail.length}`);
  pii.audit_trail.slice(0, 5).forEach((entry) => {
    console.log(`  [${entry.category}] ${(entry.reason || "").slice(0, 60)}`);
  });
}

const dl_response = await fetch(download_urls[0], {
  headers: { Authorization: `Bearer ${api_key}` },
});

const buffer = Buffer.from(await dl_response.arrayBuffer());
writeFileSync("anonymized.pdf", buffer);
console.log(`Saved as: anonymized.pdf (${buffer.length} bytes)`);
