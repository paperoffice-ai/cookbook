# Kreditorenbuchhaltung (AP Automation)

End-to-End Pipeline: Eingangsrechnungen → IDP Extraktion → Validation → CSV Export

## Workflow

```
1. PDF Upload
2. IDP Extraktion + Bounding Boxes
3. Confidence-Check (< 90% → manuelles Review)
4. Export als CSV (DATEV/Lexoffice-kompatibel)
```

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
pip install requests
```

## Verwendung

```bash
# Einzelne Rechnung
python pipeline.py invoice.pdf

# Ganzer Ordner → CSV
python pipeline.py ./rechnungen/
```

## Output

CSV mit Spalten: `vendor`, `amount`, `date`, `iban`, `filename`
