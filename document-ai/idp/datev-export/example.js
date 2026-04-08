#!/usr/bin/env node
/** PaperOffice AI — DATEV Export from Invoice IDP */
const fs = require("fs");

const api_url = "https://api.paperoffice.ai/latest/job/add/workflow";
const api_key = process.env.PAPEROFFICE_API_KEY || "";

const konto_kreditor = "70000";
const konto_bank = "1200";

async function extract_invoice(pdf_path, token = api_key) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("file_1", fs.createReadStream(pdf_path));
  form.append("model", "premium");
  form.append("idp_collection", "invoice");
  form.append("priority", "900");

  const response = await fetch(api_url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
    body: form,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
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
