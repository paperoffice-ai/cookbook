#!/usr/bin/env node
/** PaperOffice AI — Fetch weather data (FREE, costs no credits!) */

const API_URL = "https://api.paperoffice.ai/latest/location2weather";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function get_weather(lat, lon, locale = "de", token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

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

console.log(`Temperature: ${current.temp_c}°C`);
console.log(`Condition:   ${condition.text}`);
console.log(`Humidity:    ${current.humidity}%`);
console.log(`Wind:        ${current.wind_kph} km/h`);

const forecast = data.forecast || [];
if (forecast.length) {
  console.log(`\nForecast (${forecast.length} days):`);
  for (const day of forecast.slice(0, 3)) {
    const d = day.day || {};
    console.log(`  ${day.date}: ${d.condition?.text} (${d.mintemp_c}–${d.maxtemp_c}°C)`);
  }
}
