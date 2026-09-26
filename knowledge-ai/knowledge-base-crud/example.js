#!/usr/bin/env node
/** PaperOffice AI — Knowledge Base CRUD with async/await */

const BASE_URL = "https://api.paperoffice.ai/latest/knowledge";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

function headers() {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");
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

// --- CRUD Functions ---

const kb_list = () => api_get("kb_list");
const kb_create = (name, description = "", primary_language = "de") =>
  api_post("kb_add", { name, description, primary_language });
const kb_update = (kb_id, data) => api_post("kb_update", { id: kb_id, ...data });
const kb_delete = (kb_id) => api_post("kb_delete", { id: kb_id });

const article_create = (kb_id, title, content, category = "") =>
  api_post("add", { kb_id, title, content, ...(category && { category }) });
const article_list = (kb_id) => api_get(`list?kb_id=${kb_id}`);
const article_update = (article_id, data) =>
  api_post("update", { id: article_id, ...data });
const article_delete = (article_id) => api_post("delete", { id: article_id });

// --- Complete CRUD Cycle ---

// 1. Existing KBs
console.log("=== Existing Knowledge Bases ===");
const existing = await kb_list();
for (const kb of existing.data || []) {
  console.log(`  • [${kb.id}] ${kb.name} (${kb.status})`);
}

// 2. New KB
console.log("\n=== Create new KB ===");
const created = await kb_create("Cookbook-Test-KB", "Test data for cookbook example");
const kb_data = created.data || created;
const kb_id = kb_data.id || kb_data.kb_id;
console.log(`  Created: ID=${kb_id}`);

if (!kb_id) {
  console.log("⚠ No KB ID received.");
  process.exit(1);
}

// 3. Rename KB
console.log("\n=== Rename KB ===");
await kb_update(kb_id, { name: "Cookbook-Test-KB-Updated" });
console.log("  Renamed: Cookbook-Test-KB → Cookbook-Test-KB-Updated");

// 4. Create articles
console.log("\n=== Create articles ===");
const art1 = await article_create(
  kb_id,
  "Getting Started with PaperOffice",
  "PaperOffice AI provides intelligent document processing, OCR and knowledge management.",
  "Introduction"
);
const art1_id = (art1.data || art1).knowledge_id; // articles are addressed by knowledge_id (string)
console.log(`  Article 1: ID=${art1_id}`);

const art2 = await article_create(
  kb_id,
  "API Authentication",
  "All API calls require a Bearer Token in the Authorization header.",
  "Technical"
);
const art2_id = (art2.data || art2).knowledge_id;
console.log(`  Article 2: ID=${art2_id}`);

// 5. List articles
console.log("\n=== Articles in KB ===");
const articles = await article_list(kb_id);
for (const art of articles.data?.articles || []) {
  const title = art.content?.en?.title || art.content?.de?.title || art.title;
  console.log(`  • [${art.knowledge_id}] ${title}`);
}

// 6. Update article
if (art1_id) {
  console.log("\n=== Update article ===");
  await article_update(art1_id, { title: "Getting Started (updated)" });
  console.log(`  Article ${art1_id} updated.`);
}

// 7. Cleanup
console.log("\n=== Cleanup — Delete KB ===");
await kb_delete(kb_id);
console.log(`  KB ${kb_id} deleted.`);

console.log("\n✓ Complete CRUD cycle finished.");
