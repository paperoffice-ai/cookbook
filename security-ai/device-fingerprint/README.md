# Device Fingerprint — Complete Reference

Identify, verify, and track devices across sessions. The PaperOffice Fingerprint SDK provides browser fingerprinting, device verification, similarity detection, and linked device discovery.

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/fingerprint/identify` | POST | **Identify device** (v2) — full fingerprinting with enrichment |
| `/fingerprint/verify` | POST | Verify a known visitor ID |
| `/fingerprint/device` | POST | Get device details by visitor ID |
| `/fingerprint/similar` | POST | Find similar devices (fraud detection) |
| `/fingerprint/linked` | POST | Find linked devices (same network/user) |
| `/fingerprint/stats` | GET | API usage statistics |
| `/fingerprint/sdk` | GET | JavaScript SDK (global) |
| `/fingerprint/sdk.esm` | GET | JavaScript SDK (ES module) |
| `/fingerprint/sdk.min` | GET | JavaScript SDK (minified) |

**Authentication:** Bearer Token required

---

## 1. Identify device (v2)

Full device identification with optional client-side components and enrichment modules.

```
POST https://api.paperoffice.ai/latest/fingerprint/identify
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `components` | object | No | — | Client-side fingerprint components from the JS SDK (Canvas, WebGL, Audio, Fonts, Behavioral) |
| `include` | string | No | — | Comma-separated enrichment modules: `anonymity`, `currency`, or `core` for minimal response |
| `language` | string | No | `en` | Language code (ISO 639-1) for enriched data |
| `visitorId` | string | No | — | Pre-computed visitor ID from the client SDK |
| `confidence` | number | No | `0` | Client-side confidence score (0–100) |
| `botDetection` | object | No | — | Client-side bot detection data with signals array |

### Example — Server-side identification

```bash
curl -X POST "https://api.paperoffice.ai/latest/fingerprint/identify" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "visitorId": "abc123def456...",
    "include": "anonymity,currency",
    "language": "en",
    "confidence": 85,
    "botDetection": {
      "signals": ["mouse_movement", "scroll_behavior", "typing_pattern"]
    }
  }'
```

---

## 2. Verify fingerprint

Verify if a visitor ID is known and trusted.

```
POST https://api.paperoffice.ai/latest/fingerprint/verify
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `visitorId` | string | No | Visitor ID to verify |

```bash
curl -X POST "https://api.paperoffice.ai/latest/fingerprint/verify" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "visitorId": "abc123def456..." }'
```

---

## 3. Device details

Get stored details for a known device.

```
POST https://api.paperoffice.ai/latest/fingerprint/device
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | **Yes** | Visitor ID (32-character SHA-256 hash) |

---

## 4. Find similar devices

Detect potentially fraudulent device clones or account sharing.

```
POST https://api.paperoffice.ai/latest/fingerprint/similar
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `id` | string | **Yes** | — | Visitor ID of the reference device (32-char hash) |
| `threshold` | float | No | `0.7` | Similarity threshold (0.0–1.0) |

---

## 5. Get linked devices

Find devices linked through the same network, user account, or behavioral patterns.

```
POST https://api.paperoffice.ai/latest/fingerprint/linked
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | **Yes** | Visitor ID (32-char hash) |

---

## JavaScript SDK

Integrate client-side fingerprinting in your web application:

```html
<!-- Global script -->
<script src="https://api.paperoffice.ai/latest/fingerprint/sdk.min"></script>
<script>
  PaperOfficeFingerprint.identify().then(result => {
    console.log("Visitor ID:", result.visitorId);
    console.log("Confidence:", result.confidence);
  });
</script>

<!-- ES Module -->
<script type="module">
  import { identify } from "https://api.paperoffice.ai/latest/fingerprint/sdk.esm";
  const result = await identify();
</script>
```

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "visitor_abc123"

# Python
pip install requests
python3 example.py "visitor_abc123"

# Node.js (v18+)
node example.js "visitor_abc123"
```

## Expected response (verify)

```json
{
    "verified": false,
    "visitorId": "visitor_abc123",
    "reason": "unknown_device",
    "status": "success"
}
```

## Common use cases

- **Login protection:** Block unknown devices or enforce 2FA on new devices
- **Fraud detection:** Find similar/cloned devices across accounts (`/similar`)
- **Account sharing:** Detect when accounts are used from too many devices (`/linked`)
- **Bot detection:** Use client-side signals to identify automated browsers
- **Risk scoring:** Combine fingerprint confidence with anonymity detection

## See also

- [IP Geolocation](../ip-geolocation/) — Geographic location from IP
- [Anonymity Detector](../anonymity-detector/) — Detect VPN/Tor/proxy usage
- [Fake Email Detection](../fake-email-detection/) — Validate email addresses
