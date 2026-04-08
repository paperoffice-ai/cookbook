#!/usr/bin/env node
/**
 * PaperOffice AI — OCR One-Liner
 * Bearer Token ERFORDERLICH
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js document.png
 */
const fs = require("fs");

const API_URL = "https://api.paperoffice.ai/latest/job";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function ocr(file_path, mode = "complete", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(file_path));
  form.append("ocr_mode", mode); // complete | grid | text
  form.append("priority", "900");

  const response = await fetch(API_URL, {
    method: "POST",
    body: form,
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const file = process.argv[2] || "document.png";
  const result = await ocr(file);
  console.log(result?.job_result?.text || "");
})();
