#!/usr/bin/env node
/** PaperOffice AI — Convert Office documents to PDF (native MS Office)
 *
 * Pipeline: paperoffice_dataripper___office2pdf
 * Supported: DOCX, DOC, XLSX, XLS, PPTX, PPT, ODS, ODT, ODP, RTF
 * Provider: native (Windows VM + real MS Office, best quality)
 *
 * Always async — native conversion requires a Windows VM.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { basename, parse } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Error: PAPEROFFICE_API_KEY not set");
  process.exit(1);
}

const input_file = process.argv[2];
const provider = process.argv[3] ?? "native";
if (!input_file) {
  console.error("Usage: node example.js <office_file> [provider]");
  process.exit(1);
}

const headers = { Authorization: `Bearer ${api_key}` };
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function submit_job(file_path, prov = "native") {
  const buffer = readFileSync(file_path);
  const form = new FormData();
  form.append("files", new Blob([buffer]), basename(file_path));
  form.append("provider", prov);
  form.append("priority", "500");

  const response = await fetch(
    `${api_base}/job/add/paperoffice_dataripper___office2pdf`,
    { method: "POST", headers, body: form },
  );
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function poll_job(job_id, max_attempts = 60) {
  let interval = 5000;
  for (let attempt = 1; attempt <= max_attempts; attempt++) {
    await sleep(interval);
    const response = await fetch(`${api_base}/job/get/${job_id}`, { headers });
    const data = await response.json();
    const job_result = data.job_result ?? {};
    const status = job_result.status ?? data.job_status ?? "unknown";

    console.log(`  Attempt ${attempt}/${max_attempts}: ${status}`);

    if (status === "completed") return job_result;
    if (status === "failed" || status === "error") {
      throw new Error(`Job failed: ${JSON.stringify(job_result)}`);
    }
    if (attempt === 5) interval = 10000;
  }
  throw new Error(`Timeout after ${max_attempts} attempts`);
}

async function download_result(job_result, output_path) {
  const result = job_result.result ?? {};
  const files = result.files ?? result.output_files ?? [];

  let url = null;
  if (Array.isArray(files) && files.length > 0) {
    const entry = files[0];
    url = typeof entry === "string" ? entry : entry?.download_url ?? entry?.url;
  }
  url = url ?? result.download_url;

  if (!url) {
    console.log("Warning: No download URL found. Result keys:", Object.keys(result));
    return;
  }

  const dl = await fetch(url, { headers });
  const buffer = Buffer.from(await dl.arrayBuffer());
  writeFileSync(output_path, buffer);
  console.log(`Saved as: ${output_path} (${buffer.length} bytes)`);
}

console.log(`>>> Submitting office2pdf: ${input_file} (provider: ${provider})`);
const submit_data = await submit_job(input_file, provider);

if (submit_data.status !== "success") {
  console.error("Error:", JSON.stringify(submit_data, null, 2));
  process.exit(1);
}

const job_id = submit_data.job_id;
const eta = submit_data.eta ?? {};
console.log(`Job submitted: ${job_id}`);
console.log(`ETA: ${eta.estimated_completion ?? "?"} (queue pos: ${eta.queue_position ?? "?"})`);

console.log(">>> Waiting for conversion...");
const job_result = await poll_job(job_id);

const { name } = parse(input_file);
await download_result(job_result, `${name}.pdf`);
