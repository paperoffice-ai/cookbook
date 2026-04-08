#!/usr/bin/env node
/** PaperOffice AI — Entity extraction (NER) with formatted output */

const API_URL = "https://api.paperoffice.ai/latest/document_intelligence/entities";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

const EXAMPLE_TEXT =
  "Acme Corporation, based in New York, signed a contract worth " +
  "250,000 USD with Example Inc. on March 15, 2025. " +
  "Contact person is John Smith, reachable at +1 212 555 0123.";

async function extract_entities(text, entity_types = null) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ text });
  if (entity_types) params.append("entity_types", entity_types.join(","));

  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${API_KEY}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const text = process.argv[2] || EXAMPLE_TEXT;

console.log("=== Entity Extraction ===");
console.log(`Text: ${text.slice(0, 100)}...\n`);

const result = await extract_entities(text);
const entities = result.entities || [];

console.log(`Entities found: ${entities.length}\n`);

// Group by type
const grouped = {};
for (const e of entities) {
  const typ = e.type || "unknown";
  (grouped[typ] ??= []).push(e);
}

for (const [typ, items] of Object.entries(grouped)) {
  console.log(`--- ${typ.toUpperCase()} (${items.length}) ---`);
  for (const e of items) {
    const conf = ((e.confidence || 0) * 100).toFixed(0);
    console.log(`  • ${e.text.padEnd(30)} (Confidence: ${conf}%)`);
  }
  console.log();
}
