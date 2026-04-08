#!/usr/bin/env node
/**
 * PaperOffice AI — AI PDF Split (bis 3000 Seiten)
 * Bearer Token ERFORDERLICH
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js sammel_dokument.pdf
 */
const fs = require("fs");

const API_URL = "https://api.paperoffice.ai/latest/job/add/workflow";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function split_pdf(pdf_path, locale = "de_DE", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file", fs.createReadStream(pdf_path));
  form.append("template", "pdf_ai_split");
  form.append("naming_instruction", "Dokumenttyp_Datum_Absender");
  form.append("locale", locale);
  form.append("priority", "900");

  const response = await fetch(API_URL, {
    method: "POST",
    body: form,
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const pdf = process.argv[2] || "sammel_dokument.pdf";
  const data = await split_pdf(pdf);

  if (data.status !== "success") {
    console.error(`Fehler: ${data.message || "Unbekannt"}`);
    process.exit(1);
  }

  const result = data.result || {};
  console.log(`Status: ${data.status}`);
  console.log(`Schritte: ${result.total_steps || "N/A"}`);
  console.log(`Dauer: ${result.duration_ms || "N/A"}ms`);
  console.log(JSON.stringify(result, null, 2));
})();
