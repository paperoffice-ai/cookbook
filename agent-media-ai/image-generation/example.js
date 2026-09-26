#!/usr/bin/env node
/**
 * PaperOffice AI — Image Generation
 * Generates images from text prompts (up to 2048×2048)
 *
 * Usage:
 *     export PAPEROFFICE_API_KEY=po_ut_xxx
 *     node example.js "A sunset over mountains"
 *     node example.js "A sunset over mountains" premium 2
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

async function generate_image(
  prompt,
  model = "premium",
  num_images = 1,
  {
    negative_prompt = "",
    seed = -1,
    steps = 15,
    guidance_scale = 4.0,
    precompile_prompt = true,
    output = "url",
    token = API_KEY,
  } = {}
) {
  if (!token) throw new Error("PAPEROFFICE_API_KEY not set");

  const form = new FormData();
  form.append("prompt", prompt);
  form.append("model", model);
  form.append("num_images", String(num_images));
  form.append("output", output);
  form.append("precompile_prompt", String(precompile_prompt));
  form.append("seed", String(seed));
  form.append("steps", String(steps));
  form.append("guidance_scale", String(guidance_scale));
  form.append("processing_lane", "instant");
  if (negative_prompt) form.append("negative_prompt", negative_prompt);

  const response = await fetch(
    `${BASE_URL}/job/add/paperoffice_imagestudio___generate`,
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
  const prompt = process.argv[2] || "A futuristic cityscape at sunset with flying cars";
  const model = process.argv[3] || "premium";
  const num = parseInt(process.argv[4] || "1", 10);

  const data = await generate_image(prompt, model, num);
  const result = data.result || {};

  console.log(`Status:  ${data.status || "N/A"}`);

  const image_urls = result.image_urls || [];
  if (image_urls.length > 0) {
    image_urls.forEach((url, i) => console.log(`Image ${i + 1}: ${url}`));
  } else {
    console.log("No image URLs in the response");
  }

  console.log();
  console.log(JSON.stringify(data, null, 2));
})();
