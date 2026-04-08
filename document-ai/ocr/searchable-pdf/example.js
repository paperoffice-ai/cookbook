#!/usr/bin/env node
/** PaperOffice AI — Generate searchable PDF (OCR + Searchable PDF) */
import { readFileSync, writeFileSync } from "node:fs";
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

const output_file = process.argv[3] ?? "searchable_output.pdf";
const auth_headers = { Authorization: `Bearer ${api_key}` };

const form_data = new FormData();
const file_buffer = readFileSync(input_file);
const blob = new Blob([file_buffer]);
form_data.append("file_1", blob, basename(input_file));
form_data.append("ocr_mode", "text");
form_data.append("output_searchable_pdf", "true");
form_data.append("priority", "900");

const response = await fetch(
  `${api_base}/job/add/paperoffice_aiocr___generate`,
  {
    method: "POST",
    headers: auth_headers,
    body: form_data,
  }
);

const data = await response.json();
const output = data?.result?.output ?? {};
const summary = output.summary ?? {};

console.log(`Status:     ${data?.status}`);
console.log(`Pages:      ${summary.total_pages}`);
console.log(`Confidence: ${summary.avg_confidence}`);
console.log(`Duration:   ${data?.result?.duration_ms} ms`);

const pdf_url =
  output.searchable_pdf_url ??
  summary.searchable_pdf_url ??
  summary.searchable_pdf_path ??
  output.download_url;
const download_token = output.download_token ?? summary.download_token;

if (pdf_url) {
  console.log(`PDF download: ${pdf_url}`);
  const pdf_response = await fetch(pdf_url, { headers: auth_headers });
  const pdf_buffer = Buffer.from(await pdf_response.arrayBuffer());
  writeFileSync(output_file, pdf_buffer);
  console.log(`Saved: ${output_file} (${pdf_buffer.length} bytes)`);
} else if (download_token) {
  console.log(`Download token: ${download_token}`);
  const pdf_response = await fetch(
    `${api_base}/job/download/${download_token}`,
    { headers: auth_headers }
  );
  const pdf_buffer = Buffer.from(await pdf_response.arrayBuffer());
  writeFileSync(output_file, pdf_buffer);
  console.log(`Saved: ${output_file} (${pdf_buffer.length} bytes)`);
} else {
  console.log("No PDF download found in the response.");
  console.log("Full response:");
  console.log(JSON.stringify(data, null, 2));
}
