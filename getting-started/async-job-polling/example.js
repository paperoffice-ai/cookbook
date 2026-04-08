#!/usr/bin/env node
/** PaperOffice AI — Async Job-Polling (Submit → Poll → Ergebnis) */
import { readFileSync } from "node:fs";
import { basename } from "node:path";

const api_base = "https://api.paperoffice.ai/latest";
const api_key = process.env.PAPEROFFICE_API_KEY;
if (!api_key) {
  console.error("Fehler: PAPEROFFICE_API_KEY nicht gesetzt");
  process.exit(1);
}

const input_file = process.argv[2];
if (!input_file) {
  console.error("Fehler: Dateipfad als Argument übergeben");
  process.exit(1);
}

const headers = { Authorization: `Bearer ${api_key}` };

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Schritt 1: Job einreichen (priority=500 → async)
console.log(">>> Job einreichen...");
const form_data = new FormData();
const file_buffer = readFileSync(input_file);
form_data.append("file_1", new Blob([file_buffer]), basename(input_file));
form_data.append("ocr_mode", "text");
form_data.append("priority", "500");

const submit_response = await fetch(
  `${api_base}/job/add/paperoffice_aiocr___generate`,
  { method: "POST", headers, body: form_data }
);

const submit_data = await submit_response.json();
const job_id = submit_data.job_id;
if (!job_id) {
  console.error("Fehler: Keine job_id erhalten", submit_data);
  process.exit(1);
}

console.log(`Job eingereicht: ${job_id}`);

// Schritt 2: Status pollen bis fertig
console.log(">>> Warte auf Ergebnis...");
const max_attempts = 30;

for (let attempt = 1; attempt <= max_attempts; attempt++) {
  await sleep(2000);

  const poll_response = await fetch(`${api_base}/job/get/${job_id}`, {
    headers,
  });
  const poll_data = await poll_response.json();
  const status = poll_data.status ?? "unknown";

  console.log(`  Versuch ${attempt}/${max_attempts}: ${status}`);

  if (status === "completed") {
    const summary = poll_data?.result?.output?.summary ?? {};
    console.log();
    console.log("--- Ergebnis ---");
    console.log(`Seiten: ${summary.total_pages}`);
    console.log(`Zeilen: ${summary.total_lines}`);
    console.log(summary.poaiocr_extracted_fulltext ?? "Kein Text");
    process.exit(0);
  }

  if (status === "failed" || status === "error") {
    console.error("Job fehlgeschlagen!", poll_data);
    process.exit(1);
  }
}

console.error(`Timeout: Job nach ${max_attempts} Versuchen nicht fertig`);
process.exit(1);
