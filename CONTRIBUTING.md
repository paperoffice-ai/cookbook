# Contributing to PaperOffice AI Cookbook

Thanks for improving the Cookbook! This guide explains how to contribute — following our **Vibe Coding First** philosophy.

---

## Philosophy: Vibe Coding First

This Cookbook is built for the **AI-native developer workflow**:

1. **MCP First** — Connect your AI IDE to `mcp.paperoffice.ai` and let the AI discover tools natively.
2. **Postman URL First** — Paste `https://api.paperoffice.ai/latest/docs/postman` into any AI tool — it reads the full spec automatically.
3. **AI Prompts** — Use ready-to-paste prompts from `ai-prompts/` for common workflows.
4. **Recipes** — Traditional code examples as reference and fallback.

Contributions should follow this hierarchy: improve the AI experience first, traditional docs second.

---

## How to Contribute

### Adding an AI Prompt

Create a new `.md` file in `ai-prompts/`:

```markdown
# Title — What it Builds

**Tool:** Target AI tool | **Output:** What the user gets

## Prompt

\`\`\`
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

[Your prompt here]
\`\`\`

## What you get

- Bullet points of what the AI generates

## Tips

- Helpful tips for best results
```

### Adding a Recipe

Each recipe lives in its own folder with:

```
recipe-name/
├── README.md      # What, why, how, parameters, response
├── example.sh     # Bash/cURL
├── example.py     # Python (requests only)
└── example.js     # Node.js (native fetch, ESM)
```

**Rules:**

| Rule | Detail |
|------|--------|
| Language | All content in **English** |
| Python | Only `requests` — no other dependencies |
| Node.js | **ESM only** (`import`, not `require`). Uses native `fetch` and `FormData` |
| Bash | POSIX-compatible, `set -euo pipefail` |
| Auth | Always `Bearer $PAPEROFFICE_API_KEY` via env var |
| File uploads | Use the correct parameter name (`file_1` for OCR/IDP/STT, `file` for Dataripper/DMS) |
| Priority | `900` for sync examples (dev/testing), mention `500` for production |
| Comments | Only explain non-obvious logic — no narration |

### Code Style

- **snake_case** for all identifiers
- No trailing whitespace
- No hardcoded API keys — always use `$PAPEROFFICE_API_KEY`
- Scripts must be executable (`chmod +x *.sh`)

---

## Verification Checklist

Before submitting, check:

- [ ] `bash -n example.sh` — no syntax errors
- [ ] `python3 -m py_compile example.py` — compiles
- [ ] `node --check example.js` — parses
- [ ] README has correct endpoint, parameters, and response structure
- [ ] All three languages (Bash, Python, Node.js) present
- [ ] Parameter names match [Postman Collection](https://api.paperoffice.ai/latest/docs/postman)

---

## Questions?

Open an issue or connect via [paperoffice.ai/contact](https://paperoffice.ai/contact).
