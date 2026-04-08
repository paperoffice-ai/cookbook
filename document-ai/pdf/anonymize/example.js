#!/usr/bin/env node
/** PaperOffice AI — DSGVO-konforme Anonymisierung von PDF-Dokumenten */
import { readFileSync, writeFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Fehler: PAPEROFFICE_API_KEY nicht gesetzt");
  process.exit(1);
}

const input_file = process.argv[2];
const anonymize_fields = process.argv[3] ?? null;

if (!input_file) {
  console.error("Fehler: Dateipfad als Argument übergeben");
  process.exit(1);
}

// PDF hochladen und anonymisieren
const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file_1", new Blob([file_buffer]), basename(input_file));
form_data.append("template", "pdf_anonymize");
form_data.append("priority", "900");

if (anonymize_fields) {
  form_data.append("anonymize_fields", anonymize_fields);
}

const response = await fetch(`${api_base}/job/add/workflow`, {
  method: "POST",
  headers: { Authorization: `Bearer ${api_key}` },
  body: form_data,
});

const data = await response.json();
console.log(`Status: ${data?.status}`);

if (anonymize_fields) {
  console.log(`Felder: ${anonymize_fields}`);
}

if (data?.status !== "success") {
  console.error("Fehler:", JSON.stringify(data, null, 2));
  process.exit(1);
}

// Anonymisierte PDF herunterladen
const download_urls = data?.result?.files ?? [];
if (download_urls.length === 0) {
  console.error("Fehler: Keine Download-URL erhalten");
  process.exit(1);
}

const dl_response = await fetch(download_urls[0], {
  headers: { Authorization: `Bearer ${api_key}` },
});

const buffer = Buffer.from(await dl_response.arrayBuffer());
writeFileSync("anonymisiert.pdf", buffer);
console.log(`Gespeichert als: anonymisiert.pdf (${buffer.length} Bytes)`);
