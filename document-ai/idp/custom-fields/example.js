#!/usr/bin/env node
/** PaperOffice AI — IDP mit eigenen Extraktionsfeldern (Custom Fields) */
const fs = require("fs");

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

const custom_fields = [
  { name: "vertragsnummer", type: "string", description: "Vertragsnummer im Dokument" },
  { name: "kuendigungsfrist", type: "string", description: "Kündigungsfrist in Monaten oder als Datum" },
  { name: "monatlicher_betrag", type: "number", description: "Monatlicher Betrag in Euro" },
  { name: "vertragspartner", type: "string", description: "Name des Vertragspartners" },
];

async function extract_custom_fields(pdf_path, fields, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(pdf_path));
  form.append("model", "premium");
  form.append("idp_fields", JSON.stringify(fields));
  form.append("priority", "900");

  const response = await fetch(api_url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const pdf = process.argv[2];
  if (!pdf) {
    console.error("Verwendung: node example.js <datei.pdf>");
    process.exit(1);
  }

  const data = await extract_custom_fields(pdf, custom_fields);
  const pages = data?.result?.pages_idp || [];
  if (!pages.length) {
    console.log("Keine IDP-Daten gefunden");
    process.exit(1);
  }

  const fields = pages[0]?.suggested_fields || {};
  console.log(`Job-ID:  ${data.job_id ?? "—"}`);
  console.log(`Felder:  ${Object.keys(fields).length}`);
  console.log();

  for (const [name, info] of Object.entries(fields).sort(([a], [b]) => a.localeCompare(b))) {
    const value = info.value ?? "—";
    const conf = info.source_boxes_confidence ?? "—";
    console.log(`  ${name.padEnd(28)} ${(info.type ?? "—").padEnd(10)} ${String(value).padEnd(38)} [${conf}]`);
  }
})();
