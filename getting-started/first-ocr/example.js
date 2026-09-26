#!/usr/bin/env node
/** PaperOffice AI — First OCR Call (Text Extraction) */
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

const form_data = new FormData();
const file_buffer = readFileSync(input_file);
const blob = new Blob([file_buffer]);
form_data.append("file_1", blob, basename(input_file));
form_data.append("ocr_mode", "text");
form_data.append("processing_lane", "instant");

const response = await fetch(
  `${api_base}/job/add/paperoffice_aiocr___generate`,
  {
    method: "POST",
    headers: { Authorization: `Bearer ${api_key}` },
    body: form_data,
  }
);

const data = await wait_for_result(await response.json(), api_key);
const summary = data?.result?.output?.summary ?? {};

console.log(`Pages: ${summary.total_pages}`);
console.log(`Lines: ${summary.total_lines}`);
console.log(`Confidence: ${summary.avg_confidence}`);
console.log();
console.log("--- Extracted Text ---");
console.log(summary.poaiocr_extracted_fulltext ?? "No text extracted");
