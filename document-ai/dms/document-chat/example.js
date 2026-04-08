#!/usr/bin/env node
/** PaperOffice AI — Chat with a document (RAG) */

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

async function document_chat(document_id, question, context_window = null, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

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
    console.error("Usage: node example.js <document_id> <question>");
    process.exit(1);
  }

  console.log(`→ Question to document ${document_id}: ${question}`);
  const data = await document_chat(parseInt(document_id, 10), question);

  if (data.status !== "success") {
    console.error("Error:", JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.log();
  console.log("Answer:");
  console.log(data.answer ?? "—");
  console.log();

  const sources = data.sources || [];
  if (sources.length) {
    console.log(`Sources (${sources.length}):`);
    for (const s of sources) {
      const page = s.page ?? "—";
      const conf = s.confidence ?? "—";
      const text = (s.text ?? "").slice(0, 100);
      console.log(`  Page ${page} [${conf}]: ${text}`);
    }
  }
})();
