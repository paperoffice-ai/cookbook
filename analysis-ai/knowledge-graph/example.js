#!/usr/bin/env node
/** PaperOffice AI — Build and query knowledge graph */

const BASE_URL = "https://api.paperoffice.ai/latest/knowledge_graph";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

const EXAMPLE_TEXT =
  "Acme Corporation is headquartered in New York. " +
  "The CEO is John Smith. The company was founded in 2010 " +
  "and employs 500 people. Their main customer is Example Inc. from Chicago.";

async function build_graph(text) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ text });
  const response = await fetch(`${BASE_URL}/build`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${API_KEY}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function query_graph(graph_id, query) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ graph_id, query });
  const response = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${API_KEY}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const text = process.argv[2] || EXAMPLE_TEXT;

// Build graph
console.log("=== Build knowledge graph ===");
console.log(`Text: ${text.slice(0, 100)}...\n`);

const build_result = await build_graph(text);
const graph_id = build_result.graph_id || "";
const stats = build_result.stats || {};

console.log(`Graph ID:  ${graph_id}`);
console.log(`Nodes:     ${stats.nodes ?? "?"}`);
console.log(`Edges:     ${stats.edges ?? "?"}`);

const nodes = build_result.nodes || [];
if (nodes.length > 0) {
  console.log(`\nNodes (${nodes.length}):`);
  for (const node of nodes.slice(0, 10)) {
    console.log(`  • ${node.label || node.id || "?"}`);
  }
}

if (!graph_id) {
  console.log("\n⚠ No graph_id received, skipping query.");
  process.exit(0);
}

// Query graph
const question = "Who is the CEO of Acme Corporation?";
console.log(`\n=== Query knowledge graph ===`);
console.log(`Question: ${question}\n`);

const query_result = await query_graph(graph_id, question);
console.log(`Answer:     ${query_result.answer || "?"}`);
console.log(`Confidence: ${query_result.confidence || "?"}`);

const relevant = query_result.relevant_nodes || [];
if (relevant.length > 0) {
  console.log(`\nRelevant nodes:`);
  for (const node of relevant) {
    console.log(`  • ${node.label || node.id || "?"}`);
  }
}
