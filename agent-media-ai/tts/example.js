#!/usr/bin/env node
/**
 * PaperOffice AI — Text-to-Speech (TTS)
 * Converts text to natural speech (100+ voices)
 *
 * Usage:
 *     export PAPEROFFICE_API_KEY=po_ut_xxx
 *     node example.js "Hallo Welt" Nadja mp3
 */


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

async function text_to_speech(
  text,
  voice = "Nadja",
  language = "de",
  output_format = "mp3",
  speed = 1.0,
  token = API_KEY
) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const form = new FormData();
  form.append("text", text);
  form.append("voice", voice);
  form.append("language", language);
  form.append("output_format", output_format);
  form.append("output", "url");
  form.append("speed", String(speed));
  form.append("processing_lane", "instant");

  const response = await fetch(
    `${BASE_URL}/job/add/paperoffice_voice___tts`,
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
  const text = process.argv[2] || "Hallo, das ist ein Test der PaperOffice Sprachsynthese.";
  const voice = process.argv[3] || "Nadja";
  const language = process.argv[4] || "de";
  const fmt = process.argv[5] || "mp3";

  const data = await text_to_speech(text, voice, language, fmt);
  const result = data.result || {};

  console.log(`Status:   ${data.status || "N/A"}`);
  console.log(`Voice:    ${result.voice || "N/A"}`);
  console.log(`Language: ${result.language || "N/A"}`);
  console.log(`Duration: ${result.audio_duration_seconds || "N/A"}s`);
  console.log(`Size:     ${result.audio_size || "N/A"} Bytes`);
  if (result.audio_url) console.log(`URL:      ${result.audio_url}`);
  console.log();
  console.log(JSON.stringify(data, null, 2));
})();
