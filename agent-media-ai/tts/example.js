#!/usr/bin/env node
/**
 * PaperOffice AI — Text-to-Speech (TTS)
 * Wandelt Text in natürliche Sprache um (100+ Stimmen)
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js "Hallo Welt" Nadja mp3
 */

const BASE_URL = "https://api.paperoffice.ai/latest";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function text_to_speech(
  text,
  voice = "Nadja",
  output_format = "mp3",
  speed = 1.0,
  token = API_KEY
) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const form = new FormData();
  form.append("text", text);
  form.append("voice", voice);
  form.append("output_format", output_format);
  form.append("output", "url");
  form.append("speed", String(speed));
  form.append("priority", "900");

  const response = await fetch(
    `${BASE_URL}/job/add/paperoffice_voice___tts`,
    {
      method: "POST",
      body: form,
      headers: { Authorization: `Bearer ${token}` },
    }
  );

  if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  return response.json();
}

(async () => {
  const text = process.argv[2] || "Hallo, das ist ein Test der PaperOffice Sprachsynthese.";
  const voice = process.argv[3] || "Nadja";
  const fmt = process.argv[4] || "mp3";

  const data = await text_to_speech(text, voice, fmt);
  const result = data.result || {};

  console.log(`Status:   ${data.status || "N/A"}`);
  console.log(`Stimme:   ${result.voice || "N/A"}`);
  console.log(`Sprache:  ${result.language || "N/A"}`);
  console.log(`Dauer:    ${result.audio_duration_seconds || "N/A"}s`);
  console.log(`Größe:    ${result.audio_size || "N/A"} Bytes`);
  if (result.audio_url) console.log(`URL:      ${result.audio_url}`);
  console.log();
  console.log(JSON.stringify(data, null, 2));
})();
