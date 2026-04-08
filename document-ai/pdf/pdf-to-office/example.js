#!/usr/bin/env node
/** PaperOffice AI — Convert PDF to Office formats (DOCX, XLSX, PPTX)
 *
 * Pipeline: paperoffice_dataripper___pdf2office
 * Output formats: docx (default), xlsx, pptx
 *
 * Always async — conversion requires processing time.
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
const output_format = process.argv[3] ?? "docx";
if (!input_file) {
  console.error("Usage: node example.js <file.pdf> [docx|xlsx|pptx]");
  process.exit(1);
}

const headers = { Authorization: `Bearer ${api_key}` };
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function submit_job(file_path, fmt = "docx") {
  const buffer = readFileSync(file_path);
  const form = new FormData();
  form.append("file", new Blob([buffer]), basename(file_path));
  form.append("output_format", fmt);
  form.append("priority", "500");

  const response = await fetch(
    `${api_base}/job/add/paperoffice_dataripper___pdf2office`,
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
  // Download URL is at job_result.output_files[0], not inside "result"
  const output_files = job_result.output_files ?? [];
  if (!output_files.length) {
    console.log("Warning: No output_files in job_result. Keys:", Object.keys(job_result));
    return;
  }

  const dl = await fetch(output_files[0], { headers });
  const buffer = Buffer.from(await dl.arrayBuffer());
  writeFileSync(output_path, buffer);
  console.log(`Saved as: ${output_path} (${buffer.length} bytes)`);
}

console.log(`>>> Submitting pdf2office: ${input_file} → ${output_format}`);
const submit_data = await submit_job(input_file, output_format);

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
await download_result(job_result, `${name}.${output_format}`);
