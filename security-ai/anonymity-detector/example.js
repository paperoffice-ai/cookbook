#!/usr/bin/env node
/** PaperOffice AI — VPN/Proxy/Tor detection */

const API_URL = "https://api.paperoffice.ai/latest/ip2location/vpn";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function detect_anonymity(ip = null, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const payload = {};
  if (ip) payload.ip = ip;

  const params = new URLSearchParams();
  if (ip) params.set("ip", ip);
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const ip_addr = process.argv[2] || null;
const response_data = await detect_anonymity(ip_addr);
const data = response_data.vpn || response_data; // flags live under "vpn"

console.log(`VPN:        ${data.is_vpn}`);
console.log(`Proxy:      ${data.is_proxy}`);
console.log(`Tor:        ${data.is_tor}`);
console.log(`Datacenter: ${data.is_datacenter}`);
console.log(`Relay:      ${data.is_relay}`);
console.log(`Score:      ${data.score}`);
