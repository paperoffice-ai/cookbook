#!/usr/bin/env node
/** PaperOffice AI — Query and visualize knowledge graph */

const BASE_URL = "https://api.paperoffice.ai/latest/knowledge_graph";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

function headers() {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");
  return { "Authorization": `Bearer ${API_KEY}` };
}

async function get_stats() {
  const r = await fetch(`${BASE_URL}/stats`, { headers: headers() });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function query_graph(question, pofid = "", max_hops = 3) {
  const params = new URLSearchParams({ question, max_hops: String(max_hops) });
  if (pofid) params.set("pofid", pofid);

  const r = await fetch(`${BASE_URL}/universe`, {
    method: "POST",
    headers: headers(),
    body: params,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function get_mermaid(pofid = "", depth = 3) {
  const params = new URLSearchParams({ format: "mermaid", depth: String(depth) });
  if (pofid) params.set("pofid", pofid);

  const r = await fetch(`${BASE_URL}/universe`, {
    method: "POST",
    headers: headers(),
    body: params,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function get_partners(workspace_id = null, query = "") {
  const url = new URL(`${BASE_URL}/partners`);
  if (workspace_id) url.searchParams.set("workspace_id", workspace_id);
  if (query) url.searchParams.set("query", query);

  const r = await fetch(url, { headers: headers() });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

const question = process.argv[2] || "Who are the main business partners?";
const pofid = process.argv[3] || "";

// 1. Graph statistics
console.log("=== Graph statistics ===");
const stats = await get_stats();
console.log(JSON.stringify(stats, null, 2));

// 2. Query the graph
console.log(`\n=== Query: ${question} ===`);
if (pofid) console.log(`Scoped to document: ${pofid}`);

const result = await query_graph(question, pofid);
console.log(`Answer:     ${result.answer || "?"}`);
console.log(`Confidence: ${result.confidence || "?"}`);

const relevant = result.relevant_nodes || [];
if (relevant.length > 0) {
  console.log(`\nRelevant nodes (${relevant.length}):`);
  for (const node of relevant.slice(0, 10)) {
    console.log(`  - ${node.label || node.id || "?"} (${node.type || "?"})`);
  }
}

// 3. Mermaid visualization
console.log("\n=== Mermaid diagram ===");
const mermaid = await get_mermaid(pofid);
if (mermaid.graph) {
  console.log(mermaid.graph.slice(0, 500));
} else {
  console.log(JSON.stringify(mermaid, null, 2));
}

// 4. Business partners
console.log("\n=== Business partners ===");
const partners = await get_partners();
console.log(JSON.stringify(partners, null, 2));
