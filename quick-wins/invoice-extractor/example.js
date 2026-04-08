#!/usr/bin/env node
/**
 * PaperOffice AI — Invoice Extractor mit Bounding Boxes
 * Bearer Token ERFORDERLICH
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js invoice.pdf
 */
const fs = require("fs");

const API_URL = "https://api.paperoffice.ai/latest/job";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function extract_invoice(pdf_path, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(pdf_path));
  form.append("model", "premium");
  form.append("idp_collection", "invoice");
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
  const pdf = process.argv[2] || "invoice.pdf";
  const result = await extract_invoice(pdf);

  const fields = result?.job_result?.fields || {};
  for (const [name, data] of Object.entries(fields)) {
    console.log(`${name}: ${data.value} @ bbox [${data.bbox}]`);
  }
})();
