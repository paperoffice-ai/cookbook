#!/usr/bin/env node
/**
 * PaperOffice AI — Text-to-Speech Generator
 * Bearer Token ERFORDERLICH
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js "Hallo Welt" Nadja
 */

const API_URL = "https://api.paperoffice.ai/latest/job";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function text_to_speech(
  text,
  voice = "Nadja",
  output_format = "mp3",
  speed = 1.0,
  token = API_KEY
) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const FormData = (await import("form-data")).default;
  const form = new FormData();
  form.append("text", text);
  form.append("voice", voice);
  form.append("output_format", output_format);
  form.append("output", "url");
  form.append("speed", String(speed));
  form.append("priority", "999");

  const response = await fetch(API_URL, {
    method: "POST",
    body: form,
    headers: { Authorization: `Bearer ${token}`, ...form.getHeaders() },
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

(async () => {
  const text = process.argv[2] || "Hallo, das ist ein Test der Sprachausgabe.";
  const voice = process.argv[3] || "Nadja";
  const result = await text_to_speech(text, voice);
  console.log(`Audio: ${result?.job_result?.audio_url || "N/A"}`);
})();
