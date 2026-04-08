#!/usr/bin/env node
/** PaperOffice AI — Detect fake email */

const API_URL = "https://api.paperoffice.ai/latest/fakeemail/check";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function check_email(email, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

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

console.log(`Email:          ${result.email}`);
console.log(`Is fake:        ${result.is_fake}`);
console.log(`Risk score:     ${result.risk_score}`);
console.log(`Risk level:     ${result.risk_level}`);
console.log(`Recommendation: ${result.recommendation}`);
console.log(`Method:         ${result.detection_method}`);
