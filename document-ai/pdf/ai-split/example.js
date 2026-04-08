#!/usr/bin/env node
/** PaperOffice AI — Intelligentes PDF-Splitting mit KI-Erkennung */
import { readFileSync, writeFileSync } from "node:fs";
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

// PDF hochladen und KI-basiert splitten
const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file_1", new Blob([file_buffer]), basename(input_file));
form_data.append("template", "pdf_ai_split");
form_data.append("naming_instruction", "Benenne nach Dokumenttyp und Datum");
form_data.append("priority", "900");

const response = await fetch(`${api_base}/job/add/workflow`, {
  method: "POST",
  headers: { Authorization: `Bearer ${api_key}` },
  body: form_data,
});

const data = await response.json();
console.log(`Status: ${data?.status}`);

if (data?.status !== "success") {
  console.error("Fehler:", JSON.stringify(data, null, 2));
  process.exit(1);
}

const documents = data?.result?.documents ?? [];
const download_urls = data?.result?.files ?? [];
console.log(`Anzahl Teildokumente: ${documents.length}`);
console.log(`Verarbeitungsdauer:   ${data?.result?.duration_ms ?? "?"}ms\n`);

// Alle gesplitteten Dateien herunterladen
const headers = { Authorization: `Bearer ${api_key}` };

for (let i = 0; i < documents.length; i++) {
  const doc = documents[i];
  const filename = doc.suggested_filename ?? `teil_${i + 1}.pdf`;
  console.log(`  [${i + 1}] ${filename}`);
  console.log(`      Typ: ${doc.document_type ?? "?"}, Seiten: ${doc.page_range ?? "?"}`);

  if (i < download_urls.length) {
    const dl_response = await fetch(download_urls[i], { headers });
    const buffer = Buffer.from(await dl_response.arrayBuffer());
    writeFileSync(filename, buffer);
    console.log(`      → Gespeichert als: ${filename}`);
  }
}

console.log(`\nFertig — ${documents.length} Dateien heruntergeladen.`);
