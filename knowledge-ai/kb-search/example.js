#!/usr/bin/env node
/** PaperOffice AI — Knowledge Base semantische Suche */

const API_URL = "https://api.paperoffice.ai/latest/knowledge/search";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function kb_search(query, kb_id = null, limit = 5) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const data = { query, limit: String(limit) };
  if (kb_id) data.kb_id = String(kb_id);

  const params = new URLSearchParams(data);
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${API_KEY}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function print_results(results) {
  if (!results.length) {
    console.log("  Keine Ergebnisse gefunden.");
    return;
  }

  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    const score = r.score || 0;
    const bar_length = Math.round(score * 20);
    const bar = "█".repeat(bar_length) + "░".repeat(20 - bar_length);

    console.log(`  ${i + 1}. ${r.title || "Ohne Titel"}`);
    console.log(`     Score: [${bar}] ${(score * 100).toFixed(0)}%`);
    if (r.snippet) {
      console.log(`     ${r.snippet.slice(0, 120)}...`);
    }
    console.log();
  }
}

const query = process.argv[2] || "Wie funktioniert die API-Authentifizierung?";
const kb_id = process.argv[3] || null;

console.log("=== Knowledge Base Suche ===");
console.log(`Frage: ${query}`);
if (kb_id) console.log(`KB-ID: ${kb_id}`);
console.log();

const result = await kb_search(query, kb_id);
const results = result.results || [];

console.log(`Treffer: ${results.length}\n`);
print_results(results);
