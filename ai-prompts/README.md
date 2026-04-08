# AI Prompts — Vibe Coding Recipes

> **The fastest way to build with PaperOffice AI.**
>
> Paste a prompt into your AI tool. Get production code. Ship.

---

## How It Works

Every prompt follows the same pattern:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

[Your goal here]
```

The AI reads the full PaperOffice API spec (409 tools, all parameters, all response formats) and generates a complete, working solution — no manual coding required.

---

## Available Prompts

| Prompt | Best Tool | What you get |
|--------|-----------|-------------|
| [Invoice Processing Pipeline](claude-invoice-pipeline.md) | Claude | Batch invoice extraction → CSV with bounding box verification |
| [Cursor MCP Setup](cursor-mcp-setup.md) | Cursor IDE | Complete MCP config + IDE-native Document AI |
| [Voice Agent Builder](voice-agent-builder.md) | Any | TTS + STT voice agent with natural speech |
| [Fraud Detection System](fraud-detection-system.md) | Any | Device Fingerprint + IP Geolocation risk scoring |
| [Batch PDF Splitter](batch-split-3000.md) | Any | AI-powered bulk PDF splitting with smart filenames |
| [Auto-Classification System](windsurf-classifier.md) | Windsurf | Folder watcher → OCR → classify → sort documents |
| [DMS Upload + Search Pipeline](dms-pipeline.md) | Any | Upload documents → Workspace → Smart Search |
| [OCR Data Extraction](ocr-data-extraction.md) | Any | Tables + bounding boxes + structured data from scans |

---

## Tips for Best Results

1. **Always start with the Postman URL** — this gives the AI full API context.
2. **Be specific about parameters** — mention `file_1`, `priority=900`, `ocr_mode=complete` etc.
3. **Specify the output format** — "export to CSV", "return JSON", "save as PDF".
4. **Mention error handling** — "handle rate limits with retry", "check job status".
5. **Name the language** — "Create a Python script" or "Write a Node.js ESM module".

---

## Create Your Own

Use this template:

```markdown
# Title — What It Builds

**Tool:** Target AI tool | **Output:** What the user gets

## Prompt

\`\`\`
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

[Describe what you want to build]
[Be specific about endpoints, parameters, and output format]
\`\`\`

## What you get

- Point 1
- Point 2

## Tips

- Helpful tips
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full guidelines.
