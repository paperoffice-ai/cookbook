#!/usr/bin/env node
/** PaperOffice AI — Async Job Polling (Submit → Poll → Result) */
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Error: PAPEROFFICE_API_KEY not set");
  process.exit(1);
}

const input_file = process.argv[2];
if (!input_file) {
  console.error("Error: Please provide file path as argument");
  process.exit(1);
}

const headers = { Authorization: `Bearer ${api_key}` };

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Step 1: Submit job (processing_lane=sla_1h → async)
console.log(">>> Submitting job...");
const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file_1", new Blob([file_buffer]), basename(input_file));
form_data.append("ocr_mode", "text");
form_data.append("processing_lane", "sla_1h");

const submit_response = await fetch(
  `${api_base}/job/add/paperoffice_aiocr___generate`,
  { method: "POST", headers, body: form_data }
);

const submit_data = await submit_response.json();
const job_id = submit_data.job_id;
if (!job_id) {
  console.error("Error: No job_id received", submit_data);
  process.exit(1);
}

console.log(`Job submitted: ${job_id}`);

// Step 2: Poll status until completed
console.log(">>> Waiting for result...");
const max_attempts = 30;

for (let attempt = 1; attempt <= max_attempts; attempt++) {
  await sleep(2000);

  const poll_response = await fetch(`${api_base}/job/get/${job_id}`, {
    headers,
  });
  const poll_data = await poll_response.json();
  const status = poll_data.job_status ?? "unknown"; // queued | processing | completed | failed

  console.log(`  Attempt ${attempt}/${max_attempts}: ${status}`);

  if (status === "completed") {
    const summary = (poll_data.job_result ?? poll_data.result)?.output?.summary ?? {};
    console.log();
    console.log("--- Result ---");
    console.log(`Pages: ${summary.total_pages}`);
    console.log(`Lines: ${summary.total_lines}`);
    console.log(summary.poaiocr_extracted_fulltext ?? "No text");
    process.exit(0);
  }

  if (status === "failed" || status === "error") {
    console.error("Job failed!", poll_data);
    process.exit(1);
  }
}

console.error(`Timeout: Job not completed after ${max_attempts} attempts`);
process.exit(1);
