#!/usr/bin/env node
/** PaperOffice AI — Entities of a processed document, grouped by type */

const API_BASE = "https://api.paperoffice.ai/latest";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function get_document_entities(documents_id, entity_type = null, min_confidence = null) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");
  const params = new URLSearchParams({ documents_id });
  if (entity_type) params.set("type", entity_type);
  if (min_confidence !== null) params.set("min_confidence", min_confidence);

  const response = await fetch(`${API_BASE}/document_intelligence/entities?${params}`, {
    headers: { "Authorization": `Bearer ${API_KEY}` },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const documents_id = process.argv[2];
if (!documents_id) {
  console.error("Usage: node example.js <documents_id> [type] [min_confidence]\nFind documents_id with POST /documents/document-search.");
  process.exit(1);
}
const entity_type = process.argv[3] || null;
const min_conf = process.argv[4] ? parseFloat(process.argv[4]) : null;

const data = await get_document_entities(documents_id, entity_type, min_conf);
const entities = data.entities || [];
console.log(`Document:   ${data.file_name} (id ${data.document_id})`);
console.log(`Entities:   ${data.total ?? entities.length}\n`);

const grouped = {};
for (const e of entities) (grouped[e.type || "unknown"] ??= []).push(e);
for (const [typ, items] of Object.entries(grouped)) {
  console.log(`[${typ}]`);
  for (const e of items) {
    const conf = Math.round(parseFloat(e.confidence || 0) * 100);
    console.log(`  • ${String(e.value || "").padEnd(40)} (${conf}%)`);
  }
}
