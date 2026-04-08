#!/usr/bin/env node
/** PaperOffice AI — Smart document search in DMS */

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_search(query, workspace_name = "", limit = 10, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ global_search: query, limit: String(limit) });
  if (workspace_name) params.set("workspace_name", workspace_name);

  const response = await fetch(`${api_base}/documents/search`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const query = process.argv[2];
  if (!query) {
    console.error("Usage: node example.js <search_term> [workspace] [limit]");
    process.exit(1);
  }

  const workspace = process.argv[3] || "";
  const limit = parseInt(process.argv[4] || "10", 10);

  console.log(`→ Searching for: ${query}`);
  const data = await document_search(query, workspace, limit);

  if (data.status !== "success") {
    console.error("Error:", JSON.stringify(data, null, 2));
    process.exit(1);
  }

  const results = data.results || [];
  const total = data.total ?? results.length;
  console.log(`Hits: ${total}`);
  console.log();

  for (const r of results) {
    console.log(`  [${r.id ?? "—"}] ${r.filename ?? "—"} (Score: ${r.score ?? "—"})`);
    console.log(`        Workspace: ${r.workspace ?? "—"}`);
    if (r.snippet) console.log(`        ${r.snippet.slice(0, 120)}`);
    console.log();
  }
})();
