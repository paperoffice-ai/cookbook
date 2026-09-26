#!/usr/bin/env node
/**
 * PaperOffice Translate API — bulk client (hybrid wait: HTTP 200 inline, HTTP 202 → poll; optional pipeline enqueue).
 *
 * Usage:
 *   export PAPEROFFICE_API_KEY="your_bearer_token"
 *   node bulk_translate.mjs --text "Hello world" --target de
 *   node bulk_translate.mjs --json '{"title":"New lead"}' --target fr
 *   node bulk_translate.mjs --text "Save" --target es --pipeline
 *
 * API docs: https://api.paperoffice.ai/latest/docs/llms.txt
 */

const DEFAULT_API_BASE = 'https://api.paperoffice.ai/latest';
const CLIENT_WAIT_MAX_MS = 310_000;
const POLL_MAX_MS = 600_000;
const POLL_START_MS = 3_000;
const POLL_MAX_INTERVAL_MS = 10_000;

function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
}

function resolve_api_base() {
    return (process.env.PAPEROFFICE_API_BASE || DEFAULT_API_BASE).replace(/\/$/, '');
}

function resolve_token() {
    const t = process.env.PAPEROFFICE_API_KEY?.trim();
    if (!t) {
        throw new Error('Set PAPEROFFICE_API_KEY (Bearer token from https://app.paperoffice.ai)');
    }
    return t;
}

function parse_args(argv) {
    const out = { pipeline: false, source: 'en', tier: 'ultra', processing_lane: null };
    for (let i = 0; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--pipeline') out.pipeline = true;
        else if (a.startsWith('--text=')) out.text = a.slice(7);
        else if (a === '--text') out.text = argv[++i];
        else if (a.startsWith('--json=')) out.json_raw = a.slice(7);
        else if (a === '--json') out.json_raw = argv[++i];
        else if (a.startsWith('--target=')) out.target = a.slice(9);
        else if (a === '--target') out.target = argv[++i];
        else if (a.startsWith('--source=')) out.source = a.slice(9);
        else if (a === '--source') out.source = argv[++i];
        else if (a.startsWith('--lane=')) out.processing_lane = a.slice(7);
        else if (a === '--help' || a === '-h') out.help = true;
    }
    if (out.processing_lane === null) {
        out.processing_lane = out.pipeline ? 'sla_1h' : 'instant';
    }
    return out;
}

function print_help() {
    console.log(`PaperOffice Translate API example

Environment:
  PAPEROFFICE_API_KEY   Bearer token (required)
  PAPEROFFICE_API_BASE    Default: ${DEFAULT_API_BASE}

Options:
  --text <s>       Single string input
  --json <object>  JSON object input (shell-quoted)
  --target <code>  Target language (required)
  --source <code>  Source language (default: en)
  --pipeline       Use client_wait=false (enqueue + poll; for bulk jobs)
  --lane <lane>    Start-SLA: no_sla | sla_24h | sla_12h | sla_6h | sla_1h | instant
  --help

Examples:
  node bulk_translate.mjs --text "Hello" --target de
  node bulk_translate.mjs --json '{"k":"Save"}' --target fr --pipeline
`);
}

async function http_json(method, url, token, body, timeout_ms) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout_ms);
    try {
        const res = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + token
            },
            body: body ? JSON.stringify(body) : undefined,
            signal: controller.signal
        });
        const text = await res.text();
        let parsed = null;
        try {
            parsed = text ? JSON.parse(text) : null;
        } catch {
            parsed = { raw: text?.slice(0, 400) };
        }
        return { status: res.status, body: parsed };
    } finally {
        clearTimeout(timer);
    }
}

function extract_inline_translation(data) {
    const d = data?.data ?? data;
    if (!d) return null;
    if (d.translated_json !== undefined) return d.translated_json;
    if (d.translation !== undefined) return d.translation;
    if (d.translations !== undefined) return d.translations;
    return null;
}

function parse_poll_structured(structured) {
    if (!structured) return null;
    let parsed = structured;
    if (typeof structured === 'string') {
        parsed = JSON.parse(structured);
    }
    if (parsed?.translated_json !== undefined) return parsed.translated_json;
    if (parsed?.translation !== undefined) return parsed.translation;
    if (parsed?.translations !== undefined) return parsed.translations;
    return parsed;
}

async function poll_job(api_base, token, job_id) {
    const url = api_base + '/job/get/' + encodeURIComponent(job_id);
    const started = Date.now();
    let delay = POLL_START_MS;
    while (Date.now() - started < POLL_MAX_MS) {
        const { status, body } = await http_json('GET', url, token, null, 60_000);
        if (status === 429) {
            await sleep(10_000);
            continue;
        }
        const job_status = body?.job_status;
        if (['completed', 'done', 'success'].includes(job_status)) {
            return parse_poll_structured(body?.job_result?.output?.structured);
        }
        if (['failed', 'error'].includes(job_status)) {
            throw new Error(
                'Job failed [' + job_id + ']: ' + (body?.job_result?.message || job_status)
            );
        }
        await sleep(delay);
        delay = Math.min(Math.round(delay * 1.2), POLL_MAX_INTERVAL_MS);
    }
    throw new Error('Poll timeout [' + job_id + ']');
}

/**
 * Translate with hybrid client-wait (default) or pipeline enqueue mode.
 */
export async function translate(options) {
    const api_base = options.api_base ?? resolve_api_base();
    const token = options.token ?? resolve_token();
    const target_language = options.target_language;
    const source_language = options.source_language ?? 'en';
    const tier = options.tier ?? 'ultra';
    const processing_lane = options.processing_lane ?? 'instant';
    const pipeline = options.pipeline ?? false;

    const body = {
        text: options.text,
        source_language,
        target_language,
        tier,
        processing_lane,
        preserve_terms_preset: 'paperoffice_brand',
        tone: 'formal'
    };
    if (pipeline) {
        body.client_wait = false;
    }

    const submit_timeout = pipeline ? 120_000 : CLIENT_WAIT_MAX_MS;
    const submit_url = api_base + '/translate/text';

    for (let attempt = 1; attempt <= 4; attempt++) {
        let status;
        let res_body;
        try {
            ({ status, body: res_body } = await http_json(
                'POST',
                submit_url,
                token,
                body,
                submit_timeout
            ));
        } catch (e) {
            if (attempt === 4) throw e;
            if (/abort|timeout/i.test(e.message)) {
                await sleep(3000 * attempt);
                continue;
            }
            throw e;
        }

        if (status === 429) {
            const wait = res_body?.retry_after ?? res_body?.details?.retry_after ?? 15;
            await sleep(Number(wait) * 1000 || 15_000);
            continue;
        }

        const inline = extract_inline_translation(res_body);
        if (status === 200 && inline !== null && !res_body?.data?.async) {
            return { mode: 'inline', result: inline, job_id: res_body?.data?.job_id ?? null };
        }

        const d = res_body?.data ?? res_body;
        const job_id = d?.job_id ?? res_body?.job_id;
        if ((status === 202 || d?.async) && job_id) {
            const polled = await poll_job(api_base, token, job_id);
            return { mode: 'polled', result: polled, job_id };
        }
        if (job_id) {
            const polled = await poll_job(api_base, token, job_id);
            return { mode: 'polled', result: polled, job_id };
        }

        throw new Error(
            'Unexpected response HTTP ' + status + ': ' + JSON.stringify(res_body).slice(0, 400)
        );
    }
    throw new Error('translate: retries exhausted');
}

async function main() {
    const args = parse_args(process.argv.slice(2));
    if (args.help || !args.target) {
        print_help();
        process.exit(args.target ? 0 : 1);
    }

    let text;
    if (args.json_raw) {
        text = JSON.parse(args.json_raw);
    } else if (args.text) {
        text = args.text;
    } else {
        console.error('Provide --text or --json');
        process.exit(1);
    }

    const started = Date.now();
    const out = await translate({
        text,
        target_language: args.target,
        source_language: args.source,
        processing_lane: args.processing_lane,
        pipeline: args.pipeline
    });
    console.log(
        JSON.stringify(
            {
                ok: true,
                mode: out.mode,
                job_id: out.job_id,
                elapsed_ms: Date.now() - started,
                result: out.result
            },
            null,
            2
        )
    );
}

const is_main =
    process.argv[1] &&
    (process.argv[1].endsWith('translate.mjs') || process.argv[1].includes('translate'));

if (is_main) {
    main().catch((e) => {
        console.error(JSON.stringify({ ok: false, error: e.message }, null, 2));
        process.exit(1);
    });
}
