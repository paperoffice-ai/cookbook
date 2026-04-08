#!/usr/bin/env node
/** PaperOffice AI — Smart document search in DMS (Ultimate Search) */

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_search(query, workspace_id, limit = 20, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const response = await fetch(`${api_base}/documents/documents-list`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workspace_id,
      global_search: query,
      search_mode: "intelligent",
      search_preference: "balanced",
      limit,
    }),
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const query = process.argv[2];
  const workspace_id = parseInt(process.argv[3], 10);

  if (!query || isNaN(workspace_id)) {
    console.error("Usage: node example.js <search_term> <workspace_id> [limit]");
    process.exit(1);
  }

  const limit = parseInt(process.argv[4] || "20", 10);

  console.log(`-> Searching for: ${query} (workspace ${workspace_id})`);
  const data = await document_search(query, workspace_id, limit);

  if (data.status !== "success") {
    console.error("Error:", JSON.stringify(data, null, 2));
    process.exit(1);
  }

  const results = data.results || data.data || [];
  const total = data.total ?? results.length;
  console.log(`Hits: ${total}\n`);

  for (const r of results) {
    const filename = r.filename ?? r.file_name ?? "-";
    console.log(`  [${r.id ?? "-"}] ${filename} (Score: ${r.score ?? "-"})`);
    if (r.snippet) console.log(`        ${r.snippet.slice(0, 120)}`);
    console.log();
  }
})();
