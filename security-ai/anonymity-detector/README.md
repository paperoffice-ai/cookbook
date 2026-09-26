# Anonymity Detector — VPN/Proxy/Tor Detection

Detects whether an IP address is concealed via VPN, proxy, Tor, datacenter, or relay. Returns an anonymity score from 0–100%.

## Endpoint

```
POST https://api.paperoffice.ai/latest/ip2location/vpn
```

**Authentication:** VISITOR-capable (IP rate limit), recommended with Bearer token.

## Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ip` | string | ❌ | IP address (default: caller's own IP) |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_ut_xxx

# Bash — check own IP
bash example.sh

# Bash — check specific IP
bash example.sh "1.2.3.4"

# Python
pip install requests
python3 example.py "1.2.3.4"

# Node.js (v18+)
node example.js "1.2.3.4"
```

## Expected response

```json
{
  "status": "success",
  "ip": { "...": "geolocation of the address" },
  "vpn": {
    "is_vpn": false,
    "is_proxy": false,
    "is_tor": false,
    "is_datacenter": true,
    "is_relay": false,
    "score": "95.31%",
    "type": "datacenter"
  }
}
```

The anonymity flags live under `vpn`; `score` is the confidence of the classification as a percentage string.

## Reading the result

| Field | Meaning |
|---|---|
| `type` | `residential`, `datacenter`, `vpn`, `proxy`, `tor`, `relay` |
| `is_*` flags | which anonymization class matched |
| `score` | confidence of the classification (percentage) |

## Common use cases

- **Payment security:** Additionally verify VPN users during high-risk transactions
- **Content protection:** Exclude Tor users from sensitive areas
- **Risk analysis:** Incorporate anonymity score into fraud scoring models
