#!/usr/bin/env node
/** PaperOffice AI — AI-powered document generation */
const fs = require("fs");

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_generate(template, variables = {}, output_format = "pdf", token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({
    template,
    output_format,
    variables: JSON.stringify(variables),
  });

  const response = await fetch(`${api_base}/document_generation/generate`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function download_document(url, output_path, token = api_key) {
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error(`Download failed: HTTP ${response.status}`);

  const buffer = Buffer.from(await response.arrayBuffer());
  fs.writeFileSync(output_path, buffer);
  console.log(`  Saved: ${output_path}`);
}

(async () => {
  const template = process.argv[2];
  if (!template) {
    console.error("Usage: node example.js <template> [pdf|docx]");
    process.exit(1);
  }

  const output_format = process.argv[3] || "pdf";

  const variables = {
    firma: "Muster GmbH",
    rechnungsnummer: "2026-042",
    betrag: "1.250,00",
    datum: "08.04.2026",
  };

  console.log(`→ Generating document from template: ${template} (${output_format})`);
  const data = await document_generate(template, variables, output_format);

  if (data.status === "success") {
    const doc = data.document || {};
    console.log(`  Download URL: ${doc.download_url ?? "—"}`);
    console.log(`  Format:       ${doc.format ?? "—"}`);
    console.log(`  Pages:        ${doc.pages ?? "—"}`);

    if (doc.download_url) {
      const output_path = `generated.${output_format}`;
      await download_document(doc.download_url, output_path);
    }
  } else {
    console.error("Error:", JSON.stringify(data, null, 2));
  }
})();
