#!/usr/bin/env node
/** PaperOffice AI — DATEV Export from Invoice IDP */
import { readFileSync } from "node:fs";
import { basename } from "node:path";

/** HTTP 202 means the job is still running: follow job/get until it is completed. */
async function wait_for_result(data, token, api_base = "https://api.paperoffice.ai/latest", timeout_ms = 180000) {
  if (data.result || !data.job_id) return data;
  const deadline = Date.now() + timeout_ms;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 2000));
    const poll = await (await fetch(`${api_base}/job/get/${data.job_id}`, { headers: { Authorization: `Bearer ${token}` } })).json();
    if (poll.job_status === "completed" || poll.result || poll.job_result) {
      if (!poll.result && poll.job_result) poll.result = poll.job_result; // same payload, different key
      return poll;
    }
    if (poll.job_status === "failed" || poll.job_status === "error" || poll.status === "error") {
      throw new Error(`job failed: ${poll.message}`);
    }
  }
  throw new Error(`job ${data.job_id} not finished after ${timeout_ms / 1000}s`);
}

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

const konto_kreditor = "70000";
const konto_bank = "1200";

async function extract_invoice(pdf_path, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const buffer = readFileSync(pdf_path);
  const form = new FormData();
  form.append("file_1", new Blob([buffer]), basename(pdf_path));
  form.append("model", "premium");
  form.append("idp_collection", "invoice");
  form.append("processing_lane", "instant");

  const response = await fetch(api_url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return wait_for_result(await response.json(), token);
}

function get_field(fields, name, raw = false) {
  const info = fields[name] || {};
  return raw ? (info.value_raw ?? info.value ?? "") : (info.value ?? "");
}

function to_datev_date(iso_date) {
  const parts = (iso_date || "").split("-");
  if (parts.length === 3) return `${parts[2]}${parts[1]}`;
  return "";
}

function to_datev_csv(fields) {
  const umsatz = get_field(fields, "_total_amount", true);
  const datum = get_field(fields, "_invoice_date", true);
  const re_nr = get_field(fields, "_invoice_number");
  const lieferant = get_field(fields, "_supplier_name");
  const ust = get_field(fields, "_vat_rate");

  let bu_schluessel = "";
  if (ust) {
    const rate = parseFloat(String(ust).replace(",", ".").replace("%", ""));
    if (rate === 19.0) bu_schluessel = "9";
    else if (rate === 7.0) bu_schluessel = "8";
  }

  const header = [
    "Umsatz (ohne Soll/Haben-Kz)", "Soll/Haben-Kennzeichen",
    "Konto", "Gegenkonto", "BU-Schlüssel",
    "Belegdatum", "Belegfeld 1", "Buchungstext",
  ];

  const row = [umsatz, "S", konto_kreditor, konto_bank, bu_schluessel, to_datev_date(datum), re_nr, lieferant];

  return header.join(";") + "\n" + row.join(";");
}

(async () => {
  const pdf = process.argv[2];
  if (!pdf) {
    console.error("Usage: node example.js <invoice.pdf>");
    process.exit(1);
  }

  const data = await extract_invoice(pdf);
  const pages = data?.result?.pages_idp || [];
  if (!pages.length) {
    console.log("No IDP data found");
    process.exit(1);
  }

  const fields = pages[0]?.suggested_fields || {};

  console.log("--- Extracted Invoice Data ---");
  console.log(`  Invoice no.:  ${get_field(fields, "_invoice_number")}`);
  console.log(`  Date:         ${get_field(fields, "_invoice_date")}`);
  console.log(`  Supplier:     ${get_field(fields, "_supplier_name")}`);
  console.log(`  Amount:       ${get_field(fields, "_total_amount")}`);
  console.log(`  Net:          ${get_field(fields, "_net_amount")}`);
  console.log(`  VAT:          ${get_field(fields, "_vat_amount")}`);
  console.log();

  const datev_csv = to_datev_csv(fields);
  console.log("--- DATEV Accounting Entry (CSV) ---");
  console.log(datev_csv);
})();
