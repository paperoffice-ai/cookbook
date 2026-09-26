#!/usr/bin/env node
/** PaperOffice AI — Invoice Extraction (IDP Invoice) */
import { readFileSync } from "node:fs";
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

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function extract_invoice(pdf_path, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const buffer = readFileSync(pdf_path);
  const form = new FormData();
  form.append("file_1", new Blob([buffer]), basename(pdf_path));
  form.append("model", "premium");
  form.append("idp_collection", "invoice");
  form.append("processing_lane", "instant");

  const response = await fetch(api_url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return wait_for_result(await response.json(), token);
}

(async () => {
  const pdf = process.argv[2];
  if (!pdf) {
    console.error("Usage: node example.js <file.pdf>");
    process.exit(1);
  }

  const data = await extract_invoice(pdf);
  const pages = data?.result?.pages_idp || [];
  if (!pages.length) {
    console.log("No IDP data found");
    process.exit(1);
  }

  const fields = pages[0]?.suggested_fields || {};
  console.log(`Job ID:  ${data.job_id ?? "—"}`);
  console.log(`Fields:  ${Object.keys(fields).length}`);
  console.log();

  const sorted = Object.entries(fields).sort(([a], [b]) => a.localeCompare(b));
  for (const [name, info] of sorted) {
    if (info.type === "table") continue;
    const value = info.value ?? "—";
    const conf = info.source_boxes_confidence ?? "—";
    console.log(`  ${name.padEnd(30)} ${String(value).padEnd(40)} [${conf}]`);
  }
})();
