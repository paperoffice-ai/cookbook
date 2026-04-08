#!/usr/bin/env python3
"""
PaperOffice AI — Image Generation
Generates images from text prompts (up to 2048×2048)

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py "A sunset over mountains"
    python example.py "A sunset over mountains" premium 2
"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def generate_image(
    prompt: str,
    model: str = "premium",
    num_images: int = 1,
    negative_prompt: str = "",
    seed: int = -1,
    steps: int = 15,
    guidance_scale: float = 4.0,
    precompile_prompt: bool = True,
    output: str = "url",
    token: str = API_KEY,
) -> dict:
    """Generates images from a text prompt via the PaperOffice ImageStudio API."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    data = {
        "prompt": prompt,
        "model": model,
        "num_images": str(num_images),
        "output": output,
        "precompile_prompt": str(precompile_prompt).lower(),
        "seed": str(seed),
        "steps": str(steps),
        "guidance_scale": str(guidance_scale),
        "priority": "900",
    }
    if negative_prompt:
        data["negative_prompt"] = negative_prompt

    response = requests.post(
        f"{BASE_URL}/job/add/paperoffice_imagestudio___generate",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "A futuristic cityscape at sunset with flying cars"
    model = sys.argv[2] if len(sys.argv) > 2 else "premium"
    num = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    data = generate_image(prompt, model, num)

    result = data.get("result", {})
    print(f"Status:  {data.get('status', 'N/A')}")

    image_urls = result.get("image_urls", [])
    if image_urls:
        for i, url in enumerate(image_urls, 1):
            print(f"Image {i}: {url}")
    else:
        print("No image URLs in the response")

    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))
