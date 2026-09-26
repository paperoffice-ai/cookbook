#!/usr/bin/env node
/** PaperOffice AI — Knowledge Graph: statistics, question, business partners */

const BASE_URL = "https://api.paperoffice.ai/latest/knowledge_graph";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

function headers(json = false) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");
  return { Authorization: `Bearer ${API_KEY}`, ...(json ? { "Content-Type": "application/json" } : {}) };
}

async function get_stats(workspace_id) {
  const r = await fetch(`${BASE_URL}/stats?workspace_id=${workspace_id}`, { headers: headers() });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function ask(question, workspace_id, pofid = "") {
  const body = { question, workspace_id };
  if (pofid) body.pofid = pofid;
  const r = await fetch(`${BASE_URL}/ask`, { method: "POST", headers: headers(true), body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function get_partners(workspace_id, query = "") {
  const url = new URL(`${BASE_URL}/partners`);
  url.searchParams.set("workspace_id", workspace_id);
  if (query) url.searchParams.set("query", query);
  const r = await fetch(url, { headers: headers() });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

const workspace_id = process.argv[2];
if (!workspace_id) {
  console.error("Usage: node example.js <workspace_id> [question] [pofid]");
  process.exit(1);
}
const question = process.argv[3] || "Who are the main business partners?";
const pofid = process.argv[4] || "";

console.log("=== Graph statistics ===");
console.log(JSON.stringify((await get_stats(workspace_id)).stats ?? {}, null, 2).slice(0, 800));

console.log(`\n=== Question: ${question} ===`);
const result = await ask(question, workspace_id, pofid);
console.log(`Answer:  ${result.answer ?? ""}`);
console.log(`Routing: ${result.routing}`);
for (const src of (result.sources ?? []).slice(0, 5)) {
  console.log(`  source: ${src.file_name} (documents_id ${src.documents_id})`);
}

console.log("\n=== Business partners ===");
for (const p of ((await get_partners(workspace_id)).partners ?? []).slice(0, 10)) {
  console.log(`  - ${p.name}: ${p.document_count} documents`);
}
