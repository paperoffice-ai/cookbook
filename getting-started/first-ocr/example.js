#!/usr/bin/env node
/** PaperOffice AI — First OCR Call (Text Extraction) */
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

const form_data = new FormData();
const file_buffer = readFileSync(input_file);
const blob = new Blob([file_buffer]);
form_data.append("file_1", blob, basename(input_file));
form_data.append("ocr_mode", "text");
form_data.append("priority", "900");

const response = await fetch(
  `${api_base}/job/add/paperoffice_aiocr___generate`,
  {
    method: "POST",
    headers: { Authorization: `Bearer ${api_key}` },
    body: form_data,
  }
);

const data = await response.json();
const summary = data?.result?.output?.summary ?? {};

console.log(`Pages: ${summary.total_pages}`);
console.log(`Lines: ${summary.total_lines}`);
console.log(`Confidence: ${summary.avg_confidence}`);
console.log();
console.log("--- Extracted Text ---");
console.log(summary.poaiocr_extracted_fulltext ?? "No text extracted");
