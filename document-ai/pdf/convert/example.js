#!/usr/bin/env node
/** PaperOffice AI — PDF in andere Formate konvertieren */
import { readFileSync, writeFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Fehler: PAPEROFFICE_API_KEY nicht gesetzt");
  process.exit(1);
}

const input_file = process.argv[2];
const target_format = process.argv[3] ?? "docx";

if (!input_file) {
  console.error("Verwendung: node example.js datei.pdf [docx|xlsx|pptx|html|txt|jpg|png]");
  process.exit(1);
}

// PDF hochladen und konvertieren
const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file_1", new Blob([file_buffer]), basename(input_file));
form_data.append("template", "pdf_convert");
form_data.append("target_format", target_format);
form_data.append("priority", "900");

const response = await fetch(`${api_base}/job/add/workflow`, {
  method: "POST",
  headers: { Authorization: `Bearer ${api_key}` },
  body: form_data,
});

const data = await response.json();
console.log(`Status:     ${data?.status}`);
console.log(`Zielformat: ${target_format}`);

if (data?.status !== "success") {
  console.error("Fehler:", JSON.stringify(data, null, 2));
  process.exit(1);
}

// Konvertierte Datei herunterladen
const download_urls = data?.result?.files ?? [];
if (download_urls.length === 0) {
  console.error("Fehler: Keine Download-URL erhalten");
  process.exit(1);
}

const output_name = `ergebnis.${target_format}`;
const dl_response = await fetch(download_urls[0], {
  headers: { Authorization: `Bearer ${api_key}` },
});

const buffer = Buffer.from(await dl_response.arrayBuffer());
writeFileSync(output_name, buffer);
console.log(`Gespeichert als: ${output_name} (${buffer.length} Bytes)`);
