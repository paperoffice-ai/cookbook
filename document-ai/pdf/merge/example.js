#!/usr/bin/env node
/** PaperOffice AI — Mehrere PDFs zu einem Dokument zusammenfügen */
import { readFileSync, writeFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Fehler: PAPEROFFICE_API_KEY nicht gesetzt");
  process.exit(1);
}

const input_files = process.argv.slice(2);
if (input_files.length < 2) {
  console.error("Fehler: Mindestens 2 PDF-Dateien als Argumente übergeben");
  process.exit(1);
}

// Alle PDFs als file_1, file_2, ... hochladen
const form_data = new FormData();
input_files.forEach((file_path, index) => {
  const buffer = readFileSync(file_path);
  form_data.append(`file_${index + 1}`, new Blob([buffer]), basename(file_path));
});
form_data.append("template", "pdf_merge");
form_data.append("output_filename", "merged.pdf");
form_data.append("priority", "900");

const response = await fetch(`${api_base}/job/add/workflow`, {
  method: "POST",
  headers: { Authorization: `Bearer ${api_key}` },
  body: form_data,
});

const data = await response.json();
console.log(`Status: ${data?.status}`);
console.log(`Zusammengefügt: ${input_files.length} Dateien`);

if (data?.status !== "success") {
  console.error("Fehler:", JSON.stringify(data, null, 2));
  process.exit(1);
}

// Zusammengefügtes PDF herunterladen
const download_urls = data?.result?.files ?? [];
if (download_urls.length === 0) {
  console.error("Fehler: Keine Download-URL erhalten");
  process.exit(1);
}

const dl_response = await fetch(download_urls[0], {
  headers: { Authorization: `Bearer ${api_key}` },
});

const buffer = Buffer.from(await dl_response.arrayBuffer());
writeFileSync("merged.pdf", buffer);
console.log(`Gespeichert als: merged.pdf (${buffer.length} Bytes)`);
