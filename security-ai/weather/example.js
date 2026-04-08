#!/usr/bin/env node
/** PaperOffice AI — Wetterdaten abrufen (GRATIS, kostet keine Credits!) */

const API_URL = "https://api.paperoffice.ai/latest/location2weather";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function get_weather(lat, lon, locale = "de", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const params = new URLSearchParams({ lat, lon, locale });
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: params,
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

const lat = parseFloat(process.argv[2]) || 52.52;
const lon = parseFloat(process.argv[3]) || 13.41;

const data = await get_weather(lat, lon);
const current = data.current || {};
const condition = current.condition || {};

console.log(`Temperatur:      ${current.temp_c}°C`);
console.log(`Zustand:         ${condition.text}`);
console.log(`Luftfeuchtigkeit:${current.humidity}%`);
console.log(`Wind:            ${current.wind_kph} km/h`);

const forecast = data.forecast || [];
if (forecast.length) {
  console.log(`\nVorhersage (${forecast.length} Tage):`);
  for (const day of forecast.slice(0, 3)) {
    const d = day.day || {};
    console.log(`  ${day.date}: ${d.condition?.text} (${d.mintemp_c}–${d.maxtemp_c}°C)`);
  }
}
