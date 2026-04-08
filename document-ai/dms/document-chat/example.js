#!/usr/bin/env node
/** PaperOffice AI — Chat mit einem Dokument (RAG) */

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_chat(document_id, question, context_window = null, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const params = new URLSearchParams({ document_id: String(document_id), question });
  if (context_window !== null) params.set("context_window", String(context_window));

  const response = await fetch(`${api_base}/document_intelligence/chat`, {
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
  const document_id = process.argv[2];
  const question = process.argv[3];

  if (!document_id || !question) {
    console.error("Verwendung: node example.js <document_id> <frage>");
    process.exit(1);
  }

  console.log(`→ Frage an Dokument ${document_id}: ${question}`);
  const data = await document_chat(parseInt(document_id, 10), question);

  if (data.status !== "success") {
    console.error("Fehler:", JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.log();
  console.log("Antwort:");
  console.log(data.answer ?? "—");
  console.log();

  const sources = data.sources || [];
  if (sources.length) {
    console.log(`Quellen (${sources.length}):`);
    for (const s of sources) {
      const page = s.page ?? "—";
      const conf = s.confidence ?? "—";
      const text = (s.text ?? "").slice(0, 100);
      console.log(`  Seite ${page} [${conf}]: ${text}`);
    }
  }
})();
