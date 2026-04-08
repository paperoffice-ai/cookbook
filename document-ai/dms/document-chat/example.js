#!/usr/bin/env node
/** PaperOffice AI — Chat with documents via GraphRAG */

const api_base = "https://api.paperoffice.ai/latest";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function chat_with_document(question, pofid = "", max_hops = 3) {
  if (!API_KEY) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ question, max_hops: String(max_hops) });
  if (pofid) params.set("pofid", pofid);

  const response = await fetch(`${api_base}/knowledge_graph/universe`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${API_KEY}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  return response.json();
}

const question = process.argv[2];
const pofid = process.argv[3] || "";

if (!question) {
  console.log("Usage: node example.js <question> [pofid]");
  process.exit(1);
}

console.log(`Question: ${question}`);
if (pofid) console.log(`Document: ${pofid}`);
console.log();

const result = await chat_with_document(question, pofid);

console.log(`Answer: ${result.answer || "(no answer)"}`);
if (result.confidence) console.log(`Confidence: ${result.confidence}`);

const nodes = result.relevant_nodes || [];
if (nodes.length > 0) {
  console.log(`\nEvidence (${nodes.length} nodes):`);
  for (const node of nodes.slice(0, 5)) {
    console.log(`  - ${node.label || node.id || "?"} (${node.type || "?"})`);
  }
}
