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

const API_URL = "https://api.paperoffice.ai/latest/job/add/workflow";
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
  const data = await extract_invoice(pdf);

  const idp_pages = data?.result?.pages_idp || [];
  if (!idp_pages.length) {
    console.log("Keine IDP-Daten gefunden");
    process.exit(1);
  }

  const fields = idp_pages[0]?.suggested_fields || {};
  for (const [name, info] of Object.entries(fields)) {
    if (info.type === "table") continue;
    const boxes = info.source_boxes || [];
    console.log(`${name}: ${info.value} (source_boxes: ${boxes.length})`);
  }
})();
