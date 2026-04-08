#!/usr/bin/env node
/** PaperOffice AI — OCR Complete-Mode (Text + Bounding Boxes + Tabellen) */
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Fehler: PAPEROFFICE_API_KEY nicht gesetzt");
  process.exit(1);
}

const input_file = process.argv[2];
if (!input_file) {
  console.error("Fehler: Dateipfad als Argument übergeben");
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

console.log(`Status:    ${data?.status}`);
console.log(`Seiten:    ${summary.total_pages}`);
console.log(`Zeilen:    ${summary.total_lines}`);
console.log(`Zeichen:   ${summary.total_chars}`);
console.log(`Konfidenz: ${summary.avg_confidence}`);
console.log(`Dauer:     ${data?.result?.duration_ms} ms`);
console.log();

for (const [page_id, page_data] of Object.entries(pages).sort()) {
  console.log(`=== Seite ${page_id} ===`);
  console.log(`  Text-Zeilen:    ${page_data.line_count}`);
  console.log(`  Konfidenz:      ${page_data.confidence_avg}`);
  console.log(`  Sprache:        ${page_data.language?.primary}`);

  const bboxes = page_data.bounding_boxes;
  if (bboxes?.length) {
    console.log(`  Bounding Boxes: ${bboxes.length} Elemente`);
    bboxes.slice(0, 3).forEach((box, i) => {
      const text = (box.text ?? "").slice(0, 50);
      console.log(
        `    [${i}] text="${text}"  pos=(${box.x},${box.y},${box.w},${box.h})`
      );
    });
    if (bboxes.length > 3) {
      console.log(`    ... und ${bboxes.length - 3} weitere`);
    }
  }

  const tables = page_data.tables;
  if (tables?.length) {
    console.log(`  Tabellen:       ${tables.length} erkannt`);
    tables.forEach((table, i) => {
      console.log(`    Tabelle ${i}: ${table.rows?.length ?? 0} Zeilen`);
    });
  }

  console.log();
}

console.log("--- Volltext ---");
console.log(summary.poaiocr_extracted_fulltext ?? "Kein Text extrahiert");
