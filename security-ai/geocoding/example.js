#!/usr/bin/env node
/** PaperOffice AI — Geocoding (address → coordinates and vice versa) */

const FORWARD_URL = "https://api.paperoffice.ai/latest/geocoding/forward";
const REVERSE_URL = "https://api.paperoffice.ai/latest/geocoding/reverse";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function geocode_forward(address, lang = "en", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ address, lang });
  const response = await fetch(FORWARD_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function geocode_reverse(lat, lng, lang = "en", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const params = new URLSearchParams({ lat, lng, lang });
  const response = await fetch(REVERSE_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const address = process.argv[2] || "Berlin, Germany";

console.log(`=== Forward: ${address} ===`);
const fwd = await geocode_forward(address);
if (fwd.found) {
  console.log(`Lat:     ${fwd.lat}`);
  console.log(`Lng:     ${fwd.lng}`);
  console.log(`Address: ${fwd.display_name}`);
}

console.log(`\n=== Reverse: 52.5174, 13.3951 ===`);
const rev = await geocode_reverse(52.5174, 13.3951);
if (rev.found) {
  console.log(`Address: ${rev.display_name}`);
}
