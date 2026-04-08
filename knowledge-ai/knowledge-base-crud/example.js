#!/usr/bin/env node
/** PaperOffice AI — Knowledge Base CRUD mit async/await */

const BASE_URL = "https://api.paperoffice.ai/latest/knowledge";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

function headers() {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");
  return { "Authorization": `Bearer ${API_KEY}` };
}

async function api_get(endpoint) {
  const response = await fetch(`${BASE_URL}/${endpoint}`, { headers: headers() });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function api_post(endpoint, data) {
  const params = new URLSearchParams(data);
  const response = await fetch(`${BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: headers(),
    body: params,
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

// --- CRUD-Funktionen ---

const kb_list = () => api_get("kb_list");
const kb_create = (name, description = "", primary_language = "de") =>
  api_post("kb_create", { name, description, primary_language });
const kb_update = (kb_id, data) => api_post("kb_update", { kb_id, ...data });
const kb_delete = (kb_id) => api_post("kb_delete", { kb_id });

const article_create = (kb_id, title, content, category = "") =>
  api_post("article_create", { kb_id, title, content, ...(category && { category }) });
const article_list = (kb_id) => api_get(`article_list?kb_id=${kb_id}`);
const article_update = (article_id, data) =>
  api_post("article_update", { article_id, ...data });
const article_delete = (article_id) => api_post("article_delete", { article_id });

// --- Vollständiger CRUD-Zyklus ---

// 1. Bestehende KBs
console.log("=== Bestehende Knowledge Bases ===");
const existing = await kb_list();
for (const kb of existing.data || []) {
  console.log(`  • [${kb.id}] ${kb.name} (${kb.status})`);
}

// 2. Neue KB
console.log("\n=== Neue KB erstellen ===");
const created = await kb_create("Cookbook-Test-KB", "Testdaten für Cookbook-Beispiel");
const kb_data = created.data || created;
const kb_id = kb_data.id || kb_data.kb_id;
console.log(`  Erstellt: ID=${kb_id}`);

if (!kb_id) {
  console.log("⚠ Keine KB-ID erhalten.");
  process.exit(1);
}

// 3. KB umbenennen
console.log("\n=== KB umbenennen ===");
await kb_update(kb_id, { name: "Cookbook-Test-KB-Updated" });
console.log("  Umbenannt: Cookbook-Test-KB → Cookbook-Test-KB-Updated");

// 4. Artikel erstellen
console.log("\n=== Artikel erstellen ===");
const art1 = await article_create(
  kb_id,
  "Erste Schritte mit PaperOffice",
  "PaperOffice AI bietet intelligente Dokumentenverarbeitung, OCR und Knowledge Management.",
  "Einführung"
);
const art1_id = (art1.data || art1).id || art1.article_id;
console.log(`  Artikel 1: ID=${art1_id}`);

const art2 = await article_create(
  kb_id,
  "API-Authentifizierung",
  "Alle API-Aufrufe benötigen einen Bearer Token im Authorization-Header.",
  "Technik"
);
const art2_id = (art2.data || art2).id || art2.article_id;
console.log(`  Artikel 2: ID=${art2_id}`);

// 5. Artikel auflisten
console.log("\n=== Artikel in KB ===");
const articles = await article_list(kb_id);
for (const art of articles.data || []) {
  console.log(`  • [${art.id}] ${art.title}`);
}

// 6. Artikel aktualisieren
if (art1_id) {
  console.log("\n=== Artikel aktualisieren ===");
  await article_update(art1_id, { title: "Erste Schritte (aktualisiert)" });
  console.log(`  Artikel ${art1_id} aktualisiert.`);
}

// 7. Aufräumen
console.log("\n=== Aufräumen — KB löschen ===");
await kb_delete(kb_id);
console.log(`  KB ${kb_id} gelöscht.`);

console.log("\n✓ Vollständiger CRUD-Zyklus abgeschlossen.");
