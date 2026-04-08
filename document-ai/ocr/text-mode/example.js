#!/usr/bin/env node
/** PaperOffice AI — OCR Text-Mode (nur reiner Text, schnellster Modus) */
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

console.log(`Status:    ${data?.status}`);
console.log(`Seiten:    ${summary.total_pages}`);
console.log(`Zeilen:    ${summary.total_lines}`);
console.log(`Zeichen:   ${summary.total_chars}`);
console.log(`Konfidenz: ${summary.avg_confidence}`);
console.log();
console.log("--- Extrahierter Text ---");
console.log(summary.poaiocr_extracted_fulltext ?? "Kein Text extrahiert");
