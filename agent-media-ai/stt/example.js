#!/usr/bin/env node
/**
 * PaperOffice AI — Speech-to-Text (STT)
 * Transcribes audio files to text
 *
 * Usage:
 *     export PAPEROFFICE_API_KEY=po_ut_xxx
 *     node example.js audio.mp3
 *     node example.js audio.mp3 de
 */

import { readFileSync } from "node:fs";
import { basename } from "node:path";

/** HTTP 202 means the job is still running: follow job/get until it is completed. */
async function wait_for_result(data, token, api_base = "https://api.paperoffice.ai/latest", timeout_ms = 180000) {
  if (data.result || !data.job_id) return data;
  const deadline = Date.now() + timeout_ms;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 2000));
    const poll = await (await fetch(`${api_base}/job/get/${data.job_id}`, { headers: { Authorization: `Bearer ${token}` } })).json();
    if (poll.job_status === "completed" || poll.result || poll.job_result) {
      if (!poll.result && poll.job_result) poll.result = poll.job_result; // same payload, different key
      return poll;
    }
    if (poll.job_status === "failed" || poll.job_status === "error" || poll.status === "error") {
      throw new Error(`job failed: ${poll.message}`);
    }
  }
  throw new Error(`job ${data.job_id} not finished after ${timeout_ms / 1000}s`);
}

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
  form.append("processing_lane", "instant");
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
  return wait_for_result(await response.json(), token);
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
