#!/usr/bin/env node
/** PaperOffice AI — OCR Complete-Mode (text + bounding boxes + tables) */
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
form_data.append("ocr_mode", "complete");
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
const output = data?.result?.output ?? {};
const summary = output.summary ?? {};
const pages = output.pages ?? {};

console.log(`Status:     ${data?.status}`);
console.log(`Pages:      ${summary.total_pages}`);
console.log(`Lines:      ${summary.total_lines}`);
console.log(`Characters: ${summary.total_chars}`);
console.log(`Confidence: ${summary.avg_confidence}`);
console.log(`Duration:   ${data?.result?.duration_ms} ms`);
console.log();

for (const [page_id, page_data] of Object.entries(pages).sort()) {
  console.log(`=== Page ${page_id} ===`);
  console.log(`  Text lines:     ${page_data.line_count}`);
  console.log(`  Confidence:     ${page_data.confidence_avg}`);
  console.log(`  Language:       ${page_data.language?.primary}`);

  const bboxes = page_data.bounding_boxes;
  if (bboxes?.length) {
    console.log(`  Bounding Boxes: ${bboxes.length} elements`);
    bboxes.slice(0, 3).forEach((box, i) => {
      const text = (box.text ?? "").slice(0, 50);
      console.log(
        `    [${i}] text="${text}"  pos=(${box.x},${box.y},${box.w},${box.h})`
      );
    });
    if (bboxes.length > 3) {
      console.log(`    ... and ${bboxes.length - 3} more`);
    }
  }

  const tables = page_data.tables;
  if (tables?.length) {
    console.log(`  Tables:         ${tables.length} detected`);
    tables.forEach((table, i) => {
      console.log(`    Table ${i}: ${table.rows?.length ?? 0} rows`);
    });
  }

  console.log();
}

console.log("--- Full text ---");
console.log(summary.poaiocr_extracted_fulltext ?? "No text extracted");
