#!/usr/bin/env node
/**
 * PaperOffice AI — DSGVO Anonymisierung (PII Preview)
 * Bearer Token ERFORDERLICH
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js dokument.pdf
 */
const fs = require("fs");

const API_URL = "https://api.paperoffice.ai/latest/job/add/workflow";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function anonymize_preview(
  file_path,
  categories = "all",
  whitelist = null,
  token = API_KEY
) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file", fs.createReadStream(file_path));
  form.append("template", "document_anonymize_preview");
  form.append("redact_categories", categories);
  form.append("priority", "900");
  if (whitelist) form.append("whitelist", whitelist);

  const response = await fetch(API_URL, {
    method: "POST",
    body: form,
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const file = process.argv[2] || "dokument.pdf";
  const data = await anonymize_preview(file, "all", "PaperOffice");

  const result = data?.result || {};
  const boxes = result.simplified_boxes || [];
  const pii = result.detected_pii || {};
  const redacted = pii.redact_box_ids || [];

  console.log(`Gefunden: ${boxes.length} sensible Elemente`);
  console.log(`Zum Schwärzen markiert: ${redacted.length}`);
  boxes.forEach((box) => console.log(`  → ${JSON.stringify(box)}`));
})();
