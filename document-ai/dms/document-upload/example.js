#!/usr/bin/env node
/** PaperOffice AI — Dokument ins DMS hochladen */
const fs = require("fs");
const path = require("path");

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_upload(file_path, workspace_name, tags = "", token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(file_path));
  form.append("workspace_name", workspace_name);
  if (tags) form.append("tags", tags);

  const response = await fetch(`${api_base}/documents/upload`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const file_path = process.argv[2];
  const workspace = process.argv[3];

  if (!file_path || !workspace) {
    console.error("Verwendung: node example.js <datei> <workspace> [tags]");
    process.exit(1);
  }

  const tags = process.argv[4] || "";

  console.log(`→ Lade hoch: ${file_path} → Workspace: ${workspace}`);
  const data = await document_upload(file_path, workspace, tags);

  if (data.status === "success") {
    const doc = data.document || {};
    console.log(`  ID:        ${doc.id ?? "—"}`);
    console.log(`  Dateiname: ${doc.filename ?? "—"}`);
    console.log(`  Workspace: ${doc.workspace ?? "—"}`);
    console.log(`  Tags:      ${JSON.stringify(doc.tags ?? [])}`);
    console.log(`  Größe:     ${doc.size ?? "—"}`);
    console.log(`  Erstellt:  ${doc.created_at ?? "—"}`);
  } else {
    console.error("Fehler:", JSON.stringify(data, null, 2));
  }
})();
