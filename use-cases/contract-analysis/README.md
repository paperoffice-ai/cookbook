# Vertragsanalyse Pipeline

Extrahiert Key Terms aus Verträgen: Parteien, Laufzeit, Kündigungsfrist — mit Bounding Boxes für visuelle Verifikation.

## Workflow

```
1. Vertrag Upload
2. Key Terms Extraktion (IDP)
3. Bounding Box Verification
4. Confidence-basierte Alerts
```

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
pip install requests
```

## Verwendung

```bash
python pipeline.py vertrag.pdf
```

## Extrahierte Felder

| Feld | Beschreibung |
|---|---|
| `parties` | Vertragsparteien |
| `start_date` | Vertragsbeginn |
| `end_date` | Vertragsende |
| `notice_period` | Kündigungsfrist |
