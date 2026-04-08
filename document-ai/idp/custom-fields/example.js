#!/usr/bin/env node
/** PaperOffice AI — IDP with Custom Extraction Fields (Custom Fields) */
const fs = require("fs");

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

const custom_fields = [
  { name: "contract_number", type: "string", description: "Contract number in the document" },
  { name: "cancellation_period", type: "string", description: "Cancellation period in months or as a date" },
  { name: "monthly_amount", type: "number", description: "Monthly amount in euros" },
  { name: "contracting_party", type: "string", description: "Name of the contracting party" },
];

async function extract_custom_fields(pdf_path, fields, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

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
    console.error("Usage: node example.js <file.pdf>");
    process.exit(1);
  }

  const data = await extract_custom_fields(pdf, custom_fields);
  const pages = data?.result?.pages_idp || [];
  if (!pages.length) {
    console.log("No IDP data found");
    process.exit(1);
  }

  const fields = pages[0]?.suggested_fields || {};
  console.log(`Job ID:  ${data.job_id ?? "—"}`);

  const entries = Array.isArray(fields)
    ? fields.map((f) => [f.name || f.label || "—", f])
    : Object.entries(fields).sort(([a], [b]) => a.localeCompare(b));

  console.log(`Fields:  ${entries.length}`);
  console.log();

  for (const [name, info] of entries) {
    const value = info.value ?? "—";
    const conf = info.source_boxes_confidence ?? info.confidence ?? "—";
    console.log(`  ${name.padEnd(28)} ${(info.type ?? "—").padEnd(10)} ${String(value).padEnd(38)} [${conf}]`);
  }
})();
