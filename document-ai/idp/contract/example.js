#!/usr/bin/env node
/** PaperOffice AI — Contract Analysis (IDP Contract) */
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function extract_contract(pdf_path, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const buffer = readFileSync(pdf_path);
  const form = new FormData();
  form.append("file_1", new Blob([buffer]), basename(pdf_path));
  form.append("model", "ultra");
  form.append("idp_collection", "legal_document");
  form.append("priority", "900");

  const response = await fetch(api_url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const pdf = process.argv[2];
  if (!pdf) {
    console.error("Usage: node example.js <contract.pdf>");
    process.exit(1);
  }

  const data = await extract_contract(pdf);
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
    if (info.type === "table") continue;
    const value = info.value ?? "—";
    const conf = info.source_boxes_confidence ?? "—";
    console.log(`  ${name.padEnd(30)} ${String(value).padEnd(40)} [${conf}]`);
  }
})();
