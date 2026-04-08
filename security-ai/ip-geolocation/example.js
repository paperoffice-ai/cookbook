#!/usr/bin/env node
/** PaperOffice AI — Query IP geolocation */

const API_URL = "https://api.paperoffice.ai/latest/ip2location/full";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function get_geolocation(ip = null, locale = "de", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const payload = { locale };
  if (ip) payload.ip = ip;

  const params = new URLSearchParams(payload);
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const ip_addr = process.argv[2] || null;
const data = await get_geolocation(ip_addr);

console.log(JSON.stringify(data, null, 2));
