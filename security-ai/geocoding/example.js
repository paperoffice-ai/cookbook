#!/usr/bin/env node
/** PaperOffice AI — Geocoding (Adresse → Koordinaten und umgekehrt) */

const FORWARD_URL = "https://api.paperoffice.ai/latest/geocoding/forward";
const REVERSE_URL = "https://api.paperoffice.ai/latest/geocoding/reverse";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function geocode_forward(address, lang = "de", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const params = new URLSearchParams({ address, lang });
  const response = await fetch(FORWARD_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function geocode_reverse(lat, lng, lang = "de", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const params = new URLSearchParams({ lat, lng, lang });
  const response = await fetch(REVERSE_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const address = process.argv[2] || "Alexanderplatz 1, Berlin";

console.log(`=== Forward: ${address} ===`);
const fwd = await geocode_forward(address);
if (fwd.found) {
  console.log(`Lat: ${fwd.lat}`);
  console.log(`Lng: ${fwd.lng}`);
  console.log(`Adresse: ${fwd.display_name}`);
}

console.log(`\n=== Reverse: 52.52, 13.41 ===`);
const rev = await geocode_reverse(52.52, 13.41);
if (rev.found) {
  console.log(`Adresse: ${rev.display_name}`);
}
