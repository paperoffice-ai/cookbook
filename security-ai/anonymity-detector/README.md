# Anonymitäts-Detektor — VPN/Proxy/Tor-Erkennung

Erkennt ob eine IP-Adresse über VPN, Proxy, Tor, Datacenter oder Relay verschleiert wird. Liefert einen Anonymitäts-Score von 0–100%.

## Endpoint

```
POST https://api.paperoffice.ai/latest/ip2location/vpn
```

**Authentifizierung:** VISITOR-fähig (IP-Ratelimit), empfohlen mit Bearer Token.

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `ip` | string | ❌ | IP-Adresse (Standard: eigene IP des Aufrufers) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — eigene IP prüfen
bash example.sh

# Bash — bestimmte IP prüfen
bash example.sh "1.2.3.4"

# Python
pip install requests
python3 example.py "1.2.3.4"

# Node.js (v18+)
node example.js "1.2.3.4"
```

## Erwartete Antwort

```json
{
    "is_vpn": false,
    "is_proxy": false,
    "is_tor": false,
    "is_datacenter": false,
    "is_relay": false,
    "score": 0
}
```

## Score-Interpretation

| Score | Bedeutung |
|---|---|
| 0–20 | Normaler Nutzer, keine Verschleierung erkannt |
| 21–60 | Verdächtig — möglicherweise VPN oder Corporate-Proxy |
| 61–100 | Hohe Anonymität — wahrscheinlich VPN, Tor oder Datacenter |

## Anwendungsfälle

- **Zahlungssicherheit:** VPN-Nutzer bei Hochrisiko-Transaktionen zusätzlich verifizieren
- **Content-Schutz:** Tor-Nutzer von sensiblen Bereichen ausschließen
- **Risikoanalyse:** Anonymitäts-Score in Fraud-Scoring-Modelle einbeziehen
