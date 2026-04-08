#!/usr/bin/env node
/** PaperOffice AI — Intelligente Dokumentensuche im DMS */

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_search(query, workspace_name = "", limit = 10, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

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
    console.error("Verwendung: node example.js <suchbegriff> [workspace] [limit]");
    process.exit(1);
  }

  const workspace = process.argv[3] || "";
  const limit = parseInt(process.argv[4] || "10", 10);

  console.log(`→ Suche nach: ${query}`);
  const data = await document_search(query, workspace, limit);

  if (data.status !== "success") {
    console.error("Fehler:", JSON.stringify(data, null, 2));
    process.exit(1);
  }

  const results = data.results || [];
  const total = data.total ?? results.length;
  console.log(`Treffer: ${total}`);
  console.log();

  for (const r of results) {
    console.log(`  [${r.id ?? "—"}] ${r.filename ?? "—"} (Score: ${r.score ?? "—"})`);
    console.log(`        Workspace: ${r.workspace ?? "—"}`);
    if (r.snippet) console.log(`        ${r.snippet.slice(0, 120)}`);
    console.log();
  }
})();
