#!/usr/bin/env node
/**
 * PaperOffice AI — Speech-to-Text (STT)
 * Transcribes audio files to text
 *
 * Usage:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js audio.mp3
 *     node example.js audio.mp3 de
 */

import { readFileSync } from "node:fs";
import { basename } from "node:path";

const BASE_URL = "https://api.paperoffice.ai/latest";
const API_KEY = process.env.PAPEROFFICE_API_KEY || "";

async function speech_to_text(audio_path, locale = null, token = API_KEY) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const file_data = readFileSync(audio_path);
  const file_name = basename(audio_path);
  const blob = new Blob([file_data]);

  // File key is "file_1" — NOT "file"!
  const form = new FormData();
  form.append("file_1", blob, file_name);
  form.append("priority", "900");
  if (locale) form.append("locale", locale);

  const response = await fetch(
    `${BASE_URL}/job/add/paperoffice_voice___stt`,
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
  if (process.argv.length < 3) {
    console.error("Usage: node example.js <audio_file> [locale]");
    process.exit(1);
  }

  const audio_path = process.argv[2];
  const locale = process.argv[3] || null;

  const data = await speech_to_text(audio_path, locale);
  const result = data.result || {};

  console.log(`Status:   ${data.status || "N/A"}`);
  console.log(`Text:     ${result.text || "N/A"}`);
  console.log(`Language: ${result.language || "N/A"}`);
  console.log(`Duration: ${result.audio_duration_seconds || "N/A"}s`);
  console.log(`Quality:  ${result.quality || "N/A"}`);
  console.log();
  console.log(JSON.stringify(data, null, 2));
})();
