#!/usr/bin/env node
/**
 * PaperOffice AI — Text Translation
 * Translates text between 100+ languages (3 quality tiers)
 *
 * Usage:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js "Hello World" de
 *     node example.js "Hello World" de auto ultra
 */

const BASE_URL = "https://api.paperoffice.ai/latest";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function translate_text(
  text,
  target_language = "de",
  source_language = "auto",
  tier = "premium",
  token = API_KEY
) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({
    text,
    target_language,
    source_language,
    tier,
  });

  const response = await fetch(`${BASE_URL}/translate/text`, {
    method: "POST",
    body: params,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  return response.json();
}

async function list_languages(token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const response = await fetch(`${BASE_URL}/translate/languages`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const text = process.argv[2] || "Hello World";
  const target = process.argv[3] || "de";
  const source = process.argv[4] || "auto";
  const tier = process.argv[5] || "premium";

  const data = await translate_text(text, target, source, tier);
  const result = data.data || {};

  console.log(`Status:       ${data.status || "N/A"}`);
  console.log(`Translation:  ${result.translation || "N/A"}`);
  console.log(`Source lang:  ${result.source_language || "N/A"}`);
  console.log(`Target lang:  ${result.target_language || "N/A"}`);
  console.log(`Tier:         ${result.tier || "N/A"}`);
  console.log(`Characters:   ${result.characters || "N/A"}`);
  console.log();
  console.log(JSON.stringify(data, null, 2));
})();
