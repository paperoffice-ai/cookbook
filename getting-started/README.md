# Getting Started

Four recipes that cover the whole request lifecycle. Run them in this order and you have seen everything the other recipes build on.

| # | Recipe | What it shows | Token |
|---|--------|---------------|-------|
| 1 | [Hello World](hello-world/) | `GET /health` — is the API reachable, what does a response envelope look like | none (VISITOR) |
| 2 | [First OCR](first-ocr/) | Upload a PDF or image, get the text back. `200` inline result vs. `202` job | `po_ut_` / `po_gt_` |
| 3 | [Async Job Polling](async-job-polling/) | `job/add` → `job/get` → `job_status` / `job_result` — the pattern behind every long-running call | `po_ut_` / `po_gt_` |
| 4 | [Webhooks](webhooks/) | Let the API call you when a job is done instead of polling | `po_ut_` / `po_gt_` |

## Before the first call

1. Free account: [app.paperoffice.ai/en/register/](https://app.paperoffice.ai/en/register/)
2. Token: sign in → **Account → API** → create a User token (`po_ut_…`)
3. In the repo root: `cp .env.example .env` and set `PAPEROFFICE_API_KEY`

```bash
export PAPEROFFICE_API_KEY="po_ut_..."     # or source .env
bash hello-world/example.sh                 # works without a token too
python3 first-ocr/example.py invoice.pdf
node async-job-polling/example.js invoice.pdf
```

Every example is a single file with no framework: `curl`, Python `requests`, or Node `fetch`. Copy the file, change the endpoint, keep the helper.

## The one pattern to remember

```
POST job/add/<tool>   →  200  { status: "success", job_id, result | job_result }     inline, done
                      →  202  { job_id, poll_url, max_wait_seconds }                 still running, poll
GET  job/get/<job_id> →  200  { job_status: "queued|processing|completed|failed", result | job_result }
```

`202` is not an error: the API held the connection as long as it could (`client_wait=true`, default) and the job is still running. Poll `job/get` every 5–10 s until `job_status` is `completed`; polling itself is free. Read `result` (workflow / IDP / invoice) or `job_result` (OCR and most pipelines) — the recipes' `wait_for_result` helper handles both.

`processing_lane` chooses the Start-SLA (`no_sla` … `instant`) and with it the credit factor and how likely you get `200` inline. Details in [Pro Tips](../pro-tips/).

## Next

- Extract structured data instead of text → [Document AI / IDP](../document-ai/idp/)
- Store, search and chat with documents → [Document AI / DMS](../document-ai/dms/)
- Let Claude, ChatGPT or Cursor call the API for you → [MCP](../mcp/)
- Stuck → [Help & FAQ](https://help.paperoffice.ai/) · [Issues](https://github.com/paperoffice-ai/cookbook/issues)
