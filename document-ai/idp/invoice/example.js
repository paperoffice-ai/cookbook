#!/usr/bin/env node
/** PaperOffice AI — Rechnungs-Extraktion (IDP Invoice) */
const fs = require("fs");
const path = require("path");

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function extract_invoice(pdf_path, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(pdf_path));
  form.append("model", "premium");
  form.append("idp_collection", "invoice");
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

  const data = await extract_invoice(pdf);
  const pages = data?.result?.pages_idp || [];
  if (!pages.length) {
    console.log("Keine IDP-Daten gefunden");
    process.exit(1);
  }

  const fields = pages[0]?.suggested_fields || {};
  console.log(`Job-ID:  ${data.job_id ?? "—"}`);
  console.log(`Felder:  ${Object.keys(fields).length}`);
  console.log();

  const sorted = Object.entries(fields).sort(([a], [b]) => a.localeCompare(b));
  for (const [name, info] of sorted) {
    if (info.type === "table") continue;
    const value = info.value ?? "—";
    const conf = info.source_boxes_confidence ?? "—";
    console.log(`  ${name.padEnd(30)} ${String(value).padEnd(40)} [${conf}]`);
  }
})();
