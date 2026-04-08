#!/usr/bin/env node
/**
 * PaperOffice AI — Bildgenerierung
 * Erzeugt Bilder aus Text-Prompts (bis 2048×2048)
 *
 * Verwendung:
 *     export PAPEROFFICE_API_KEY=po_sk_xxx
 *     node example.js "A sunset over mountains"
 *     node example.js "A sunset over mountains" premium 2
 */

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
  if (!token) throw new Error("PAPEROFFICE_API_KEY nicht gesetzt");

  const form = new FormData();
  form.append("prompt", prompt);
  form.append("model", model);
  form.append("num_images", String(num_images));
  form.append("output", output);
  form.append("precompile_prompt", String(precompile_prompt));
  form.append("seed", String(seed));
  form.append("steps", String(steps));
  form.append("guidance_scale", String(guidance_scale));
  form.append("priority", "900");
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
  return response.json();
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
    image_urls.forEach((url, i) => console.log(`Bild ${i + 1}:  ${url}`));
  } else {
    console.log("Keine Bild-URLs in der Antwort");
  }

  console.log();
  console.log(JSON.stringify(data, null, 2));
})();
