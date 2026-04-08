#!/usr/bin/env node
/** PaperOffice AI — Identity Document Extraction (IDP Identity) */
const fs = require("fs");

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function extract_identity(file_path, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(file_path));
  form.append("model", "premium");
  form.append("idp_collection", "identity_document");
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
  const file = process.argv[2];
  if (!file) {
    console.error("Usage: node example.js <id_card.pdf>");
    process.exit(1);
  }

  const data = await extract_identity(file);
  const pages = data?.result?.pages_idp || [];
  if (!pages.length) {
    console.log("No IDP data found");
    process.exit(1);
  }

  const fields = pages[0]?.suggested_fields || {};
  console.log(`Job ID:  ${data.job_id ?? "—"}`);
  console.log(`Fields:  ${Object.keys(fields).length}`);
  console.log();

  for (const [name, info] of Object.entries(fields).sort(([a], [b]) => a.localeCompare(b))) {
    const value = info.value ?? "—";
    const conf = info.source_boxes_confidence ?? "—";
    console.log(`  ${name.padEnd(30)} ${String(value).padEnd(40)} [${conf}]`);
  }
})();
