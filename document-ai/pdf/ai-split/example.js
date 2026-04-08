#!/usr/bin/env node
/** PaperOffice AI — Intelligent PDF splitting with AI detection */
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

// Upload PDF and split using AI
const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file_1", new Blob([file_buffer]), basename(input_file));
form_data.append("template", "pdf_ai_split");
form_data.append("naming_instruction", "Name by document type and date");
form_data.append("priority", "900");

const response = await fetch(`${api_base}/job/add/workflow`, {
  method: "POST",
  headers: { Authorization: `Bearer ${api_key}` },
  body: form_data,
});

const data = await response.json();
console.log(`Status: ${data?.status}`);

if (data?.status !== "success") {
  console.error("Error:", JSON.stringify(data, null, 2));
  process.exit(1);
}

const documents = data?.result?.documents ?? [];
const download_urls = data?.result?.files ?? [];
console.log(`Number of sub-documents: ${documents.length}`);
console.log(`Processing duration:     ${data?.result?.duration_ms ?? "?"}ms\n`);

// Download all split files
const headers = { Authorization: `Bearer ${api_key}` };

for (let i = 0; i < documents.length; i++) {
  const doc = documents[i];
  const filename = doc.suggested_filename ?? `part_${i + 1}.pdf`;
  console.log(`  [${i + 1}] ${filename}`);
  console.log(`      Type: ${doc.document_type ?? "?"}, Pages: ${doc.page_range ?? "?"}`);

  if (i < download_urls.length) {
    const dl_response = await fetch(download_urls[i], { headers });
    const buffer = Buffer.from(await dl_response.arrayBuffer());
    writeFileSync(filename, buffer);
    console.log(`      → Saved as: ${filename}`);
  }
}

console.log(`\nDone — ${documents.length} files downloaded.`);
