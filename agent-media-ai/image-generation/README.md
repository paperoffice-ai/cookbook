# Image Generation

Generates images from text prompts using PaperOffice ImageStudio. Three model tiers with customizable resolution, aspect ratio, and advanced generation controls.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate
```

**Authentication:** Bearer Token required

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh "A sunset over mountains" premium 1

# Python
pip install requests
python3 example.py "A sunset over mountains" premium 2

# Node.js (v18+)
node example.js "A sunset over mountains" premium 1
```

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `prompt` | string | **Yes** | — | Image description (English recommended for best results) |
| `model` | string | **Yes** | `premium` | Model tier: `basic`, `premium`, `ultra` |
| `width` | int | No | 1024 | Image width in pixels (128–2048, tier-dependent) |
| `height` | int | No | 1024 | Image height in pixels (128–2048, tier-dependent) |
| `num_images` | int | No | `1` | Number of images to generate (1–8) |
| `negative_prompt` | string | No | — | Elements to exclude (e.g. `"blurry, watermark"`) |
| `seed` | int | No | `-1` | Seed for reproducibility (`-1` = random) |
| `steps` | int | No | `15` | Diffusion steps (1–50, more = more detail, slower) |
| `guidance_scale` | float | No | `4.0` | Prompt adherence (1.0–20.0, higher = stricter) |
| `precompile_prompt` | bool | No | `true` | AI prompt optimization (recommended) |
| `output` | string | No | `url` | `url`, `base64`, `inline` |
| `priority` | int | No | — | `≥ 900` for synchronous processing |

## Model tiers & resolution limits

| Model | Max resolution | Default | Cost | Best for |
|---|---|---|---|---|
| `basic` | 512 × 512 | 512 × 512 | Lowest | Quick previews, prototyping |
| `premium` | 1280 × 1280 | 1024 × 1024 | Medium | Standard production use |
| `ultra` | 2048 × 2048 | 1536 × 1536 | Highest | Print material, high-quality assets |

## Aspect ratio presets

Use `width` and `height` to control the aspect ratio:

| Aspect ratio | Width | Height | Example use case |
|---|---|---|---|
| Square (1:1) | 1024 | 1024 | Social media, icons |
| Landscape (16:9) | 1280 | 720 | Banners, headers, presentations |
| Portrait (9:16) | 720 | 1280 | Mobile wallpapers, stories |
| Icon (1:1) | 512 | 512 | App icons, favicons |
| Panoramic (21:9) | 1280 | 549 | Ultra-wide banners |

## Response example

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "image_urls": [
      "https://api.paperoffice.ai/latest/job/download/..."
    ],
    "output_mode": "url"
  }
}
```

## Advanced examples

### Landscape banner (16:9)

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "prompt=A panoramic mountain range at sunrise, dramatic clouds" \
  -F "model=premium" \
  -F "width=1280" \
  -F "height=720" \
  -F "priority=999"
```

### High-quality with custom steps

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "prompt=Oil painting of a serene lake at dusk, impressionist style" \
  -F "model=ultra" \
  -F "width=1536" \
  -F "height=1536" \
  -F "steps=25" \
  -F "guidance_scale=7.5" \
  -F "priority=999"
```

### Reproducible output with seed

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "prompt=A majestic dragon over a castle" \
  -F "model=premium" \
  -F "seed=42" \
  -F "precompile_prompt=false" \
  -F "priority=999"
```

> **Note:** Set `precompile_prompt=false` when using a fixed seed, otherwise the AI-optimized prompt may differ between runs.

### Batch generation

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "prompt=Futuristic cityscape at night, cyberpunk" \
  -F "model=premium" \
  -F "num_images=4" \
  -F "priority=999"
```

> Each image in a batch is billed individually.

## Remove Background

Separate endpoint for background removal:

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___remove_bg
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | file | **Yes** | — | Image file (PNG, JPG, WEBP) — **note: `file`, not `file_1`!** |
| `output` | string | No | `url` | `url`, `base64`, `inline` |
| `priority` | int | No | — | `≥ 900` for synchronous processing |

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___remove_bg" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file=@photo.png" \
  -F "output=url" \
  -F "priority=999"
```

## Prompt Precompiler

With `precompile_prompt=true` (default), your prompt is automatically enhanced by the PaperOffice image precompiler. This adds quality-improving keywords, style guidance, and technical specifications — better results without manual prompt engineering.

Set `precompile_prompt=false` to send your exact prompt to the model unchanged (useful for precise control or reproducibility with seeds).

## Tips

- **English prompts** generally yield better results than other languages
- **Negative prompts** like `"blurry, low quality, distorted, watermark"` dramatically improve output
- **Guidance scale** between 3.0–7.0 works best for most prompts
- **Steps:** 15 is fast and good; 25–50 gives more detail but slower
- **Batch billing:** `num_images=4` costs 4× the single-image price

## See also

- [Translation](../translation/) — Translate prompts to English for better results
