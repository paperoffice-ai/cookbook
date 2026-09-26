# Currency Exchange — Exchange Rates

Fetches current exchange rates for 172+ currencies. Supports conversion from and to any ISO 4217 currency with an optional amount.

## Endpoint

```
POST https://api.paperoffice.ai/latest/currency_exchange/get_rates
```

**Authentication:** VISITOR-capable (no token required, but IP rate limit). No limit with Bearer token.

## Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `base` | string | ✅ | Base currency (ISO 4217, e.g. `EUR`) |
| `symbols` | string | ❌ | Target currency or comma-separated list (without = all currencies) |
| `amount` | float | ❌ | Amount to convert (default: `1`) |

## How to run

```bash
# No token required!

# Bash — 100 EUR to all currencies
bash example.sh EUR "" 100

# Bash — EUR to USD
bash example.sh EUR USD 250

# Python
pip install requests
python3 example.py EUR USD 100

# Node.js (v18+)
node example.js EUR USD 100
```

## Expected response

```json
{
    "base": "EUR",
    "amount": 100,
    "rates": {
        "USD": 115.86,
        "GBP": 86.12,
        "CHF": 95.43,
        "JPY": 16234.50
    },
    "currencies_count": 172
}
```

## Common use cases

- **E-commerce:** Display prices in the customer's local currency
- **Invoicing:** Automatically convert international invoices
- **Financial dashboards:** Embed live exchange rates in overviews
- **Travel expenses:** Convert expense reports to home currency
