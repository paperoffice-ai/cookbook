#!/usr/bin/env node
/** PaperOffice AI — USt-ID validieren */

const API_URL = "https://api.paperoffice.ai/latest/vat/validate";
const RATES_URL = "https://api.paperoffice.ai/latest/vat/rates";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function validate_vat(vat_id, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const params = new URLSearchParams({ vat_id });
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function get_vat_rates() {
  const response = await fetch(RATES_URL);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const vat = process.argv[2] || "DE123456789";

console.log(`=== USt-ID Validierung: ${vat} ===`);
const result = await validate_vat(vat);
console.log(`Status:        ${result.status}`);
console.log(`Format gültig: ${result.format_valid}`);
if (result.error) {
  console.log(`Fehler:        ${result.error}`);
  console.log(`Nachricht:     ${result.message}`);
  console.log(`Layer:         ${result.layer}`);
}

console.log(`\n=== EU-Steuersätze ===`);
const rates = await get_vat_rates();
console.log(JSON.stringify(rates, null, 2).slice(0, 500));
