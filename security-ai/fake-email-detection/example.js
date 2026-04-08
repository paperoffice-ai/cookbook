#!/usr/bin/env node
/** PaperOffice AI — Fake-E-Mail erkennen */

const API_URL = "https://api.paperoffice.ai/latest/fakeemail/check";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function check_email(email, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const params = new URLSearchParams({ email });
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const email = process.argv[2] || "test@mailinator.com";
const data = await check_email(email);
const result = data.result || {};

console.log(`E-Mail:       ${result.email}`);
console.log(`Ist Fake:     ${result.is_fake}`);
console.log(`Risiko-Score: ${result.risk_score}`);
console.log(`Risiko-Level: ${result.risk_level}`);
console.log(`Empfehlung:   ${result.recommendation}`);
console.log(`Methode:      ${result.detection_method}`);
