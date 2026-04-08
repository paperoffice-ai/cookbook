#!/usr/bin/env node
/** PaperOffice AI — Wechselkurse abfragen (VISITOR-fähig, optional mit Token) */

const API_KEY = process.env.PAPEROFFICE_API_KEY || "";
const API_URL = "https://api.paperoffice.ai/latest/currency_exchange/get_rates";

async function get_exchange_rates(from_currency = "EUR", to_currency = null, amount = 1) {
  const params = new URLSearchParams({ from: from_currency, amount });
  if (to_currency) params.set("to", to_currency);

  const headers = {};
  if (API_KEY) headers["Authorization"] = `Bearer ${API_KEY}`;

  const response = await fetch(API_URL, {
    method: "POST",
    headers,
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const from_cur = process.argv[2] || "EUR";
const to_cur = process.argv[3] || null;
const amount = parseFloat(process.argv[4]) || 100;

const data = await get_exchange_rates(from_cur, to_cur, amount);

console.log(`Basis:     ${data.base}`);
console.log(`Betrag:    ${data.amount}`);
console.log(`Währungen: ${data.currencies_count}`);

const top_currencies = ["USD", "GBP", "CHF", "JPY", "CNY"];
for (const cur of top_currencies) {
  if (data.rates?.[cur]) {
    console.log(`  ${cur}: ${data.rates[cur]}`);
  }
}
