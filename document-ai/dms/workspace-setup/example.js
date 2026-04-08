#!/usr/bin/env node
/** PaperOffice AI — Workspace erstellen & auflisten */

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function workspace_create(name, description = "", token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const response = await fetch(`${api_base}/documents/workspace_create`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ name, description }),
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function workspace_list(token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const response = await fetch(`${api_base}/documents/workspace_list`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const name = process.argv[2] || "Mein Workspace";
  const desc = process.argv[3] || "Automatisch erstellter Workspace";

  console.log(`→ Erstelle Workspace: ${name}`);
  const create_data = await workspace_create(name, desc);

  if (create_data.status === "success") {
    const ws = create_data.workspace || {};
    console.log(`  ID:           ${ws.id ?? "—"}`);
    console.log(`  Name:         ${ws.name ?? "—"}`);
    console.log(`  Beschreibung: ${ws.description ?? "—"}`);
    console.log(`  Erstellt:     ${ws.created_at ?? "—"}`);
  } else {
    console.error("Fehler:", JSON.stringify(create_data, null, 2));
  }

  console.log();
  console.log("→ Alle Workspaces auflisten");
  const list_data = await workspace_list();

  const workspaces = list_data.workspaces || [];
  console.log(`Gefunden: ${workspaces.length} Workspace(s)`);
  console.log();
  for (const ws of workspaces) {
    console.log(`  [${ws.id ?? "—"}] ${ws.name ?? "—"} — ${ws.description ?? ""}`);
  }
})();
