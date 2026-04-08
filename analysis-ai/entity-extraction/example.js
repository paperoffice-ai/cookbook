#!/usr/bin/env node
/** PaperOffice AI — Entity-Extraktion (NER) mit formatierter Ausgabe */

const API_URL = "https://api.paperoffice.ai/latest/document_intelligence/entities";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

const BEISPIEL_TEXT =
  "Die Mustermann GmbH mit Sitz in München hat am 15. März 2025 " +
  "einen Vertrag über 250.000 EUR mit der Beispiel AG abgeschlossen. " +
  "Ansprechpartner ist Max Mustermann, erreichbar unter +49 89 123456.";

async function extract_entities(text, entity_types = null) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

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

const text = process.argv[2] || BEISPIEL_TEXT;

console.log("=== Entity-Extraktion ===");
console.log(`Text: ${text.slice(0, 100)}...\n`);

const result = await extract_entities(text);
const entities = result.entities || [];

console.log(`Gefundene Entitäten: ${entities.length}\n`);

// Nach Typ gruppieren
const grouped = {};
for (const e of entities) {
  const typ = e.type || "unknown";
  (grouped[typ] ??= []).push(e);
}

for (const [typ, items] of Object.entries(grouped)) {
  console.log(`--- ${typ.toUpperCase()} (${items.length}) ---`);
  for (const e of items) {
    const conf = ((e.confidence || 0) * 100).toFixed(0);
    console.log(`  • ${e.text.padEnd(30)} (Konfidenz: ${conf}%)`);
  }
  console.log();
}
