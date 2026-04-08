#!/usr/bin/env node
/** PaperOffice AI — Upload document to DMS */
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_upload(file_path, workspace_name, tags = "", token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const buffer = readFileSync(file_path);
  const form = new FormData();
  form.append("file", new Blob([buffer]), basename(file_path));
  form.append("workspace_name", workspace_name);
  if (tags) form.append("tags", tags);

  const response = await fetch(`${api_base}/documents/document-put`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const file_path = process.argv[2];
  const workspace = process.argv[3];

  if (!file_path || !workspace) {
    console.error("Usage: node example.js <file> <workspace> [tags]");
    process.exit(1);
  }

  const tags = process.argv[4] || "";

  console.log(`→ Uploading: ${file_path} → Workspace: ${workspace}`);
  const data = await document_upload(file_path, workspace, tags);

  if (data.status === "success") {
    const doc = data.document || {};
    console.log(`  ID:        ${doc.id ?? "—"}`);
    console.log(`  Filename:  ${doc.filename ?? "—"}`);
    console.log(`  Workspace: ${doc.workspace ?? "—"}`);
    console.log(`  Tags:      ${JSON.stringify(doc.tags ?? [])}`);
    console.log(`  Size:      ${doc.size ?? "—"}`);
    console.log(`  Created:   ${doc.created_at ?? "—"}`);
  } else {
    console.error("Error:", JSON.stringify(data, null, 2));
  }
})();
