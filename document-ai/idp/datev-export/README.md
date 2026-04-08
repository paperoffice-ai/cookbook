# DATEV-Export aus Rechnungs-IDP

Extrahiert Rechnungsdaten via IDP und konvertiert sie automatisch in einen **DATEV-kompatiblen Buchungssatz** (CSV-Format für DATEV Unternehmen Online / Kanzlei-Rechnungswesen).

## Workflow

```
PDF-Rechnung → PaperOffice IDP (invoice) → DATEV Buchungsstapel (CSV)
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter         | Wert       | Beschreibung                         |
|-------------------|------------|--------------------------------------|
| `file_1`          | Datei      | PDF der Rechnung                     |
| `model`           | `premium`  | Extraktionsqualität                  |
| `idp_collection`  | `invoice`  | Rechnungs-Extraktion                 |
| `priority`        | `900`      | Synchrone Verarbeitung (≥900)        |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash — gibt DATEV-CSV auf stdout aus
bash example.sh rechnung.pdf

# Python — mit formatierter Ausgabe + CSV
python3 example.py rechnung.pdf

# Python — direkt in CSV-Datei schreiben
python3 example.py rechnung.pdf > buchung.csv

# Node.js
npm install form-data
node example.js rechnung.pdf
```

## DATEV Buchungsstapel-Format

Das generierte CSV folgt dem **DATEV-Buchungsstapel** Format:

| Spalte                           | Beispiel         | Quelle (IDP-Feld)       |
|----------------------------------|------------------|--------------------------|
| Umsatz (ohne Soll/Haben-Kz)     | `1469.06`        | `_total_amount.value_raw`|
| Soll/Haben-Kennzeichen           | `S`              | Fest: Soll               |
| Konto                            | `70000`          | Kreditor (anpassbar)     |
| Gegenkonto                       | `1200`           | Bank (anpassbar)         |
| BU-Schlüssel                     | `9`              | Aus `_vat_rate` abgeleitet|
| Belegdatum                       | `1503`           | `_invoice_date` → DDMM  |
| Belegfeld 1                      | `2024-001`       | `_invoice_number`        |
| Buchungstext                     | `Mustermann GmbH`| `_supplier_name`         |

### BU-Schlüssel Mapping

| USt-Satz | BU-Schlüssel | Bedeutung                    |
|----------|-------------|------------------------------|
| 19%      | `9`         | Vorsteuer 19%                |
| 7%       | `8`         | Vorsteuer 7%                 |
| Sonstige | (leer)      | Manuell zuordnen             |

### Kontenrahmen

Die Beispiele nutzen **SKR04** als Standard:

| Konto  | Bedeutung                         |
|--------|-----------------------------------|
| 70000  | Kreditor (Sammelkonto)            |
| 1200   | Bank                              |

Für **SKR03** die Kontonummern in den Beispielen anpassen (z.B. Konto `1800` für Bank).

## Beispiel-Ausgabe

```
--- Extrahierte Rechnungsdaten ---
  Rechnungsnr:  2024-001
  Datum:        2024-03-15
  Lieferant:    Mustermann GmbH
  Betrag:       1.469,06
  Netto:        1.234,50
  USt:          234,56

--- DATEV Buchungssatz (CSV) ---
Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;Konto;Gegenkonto;BU-Schlüssel;Belegdatum;Belegfeld 1;Buchungstext
1469.06;S;70000;1200;9;1503;2024-001;Mustermann GmbH
```

## Erweiterungsmöglichkeiten

- **Batch-Verarbeitung**: Schleife über mehrere PDFs → ein zusammengefasster Buchungsstapel
- **Konten-Mapping**: Lieferantenname → Kreditor-Konto aus Stammdaten auflösen
- **Validierung**: IBAN/USt-IdNr. gegen PaperOffice Validierungs-APIs prüfen
- **DATEV XML**: Für komplexere Szenarien das DATEV-XML-Format statt CSV nutzen

## Tipps

- **`value_raw`** für Beträge verwenden (Punkt als Dezimaltrenner, DATEV-konform)
- DATEV erwartet das Belegdatum im Format **DDMM** (ohne Jahr, da im Header definiert)
- Bei Gutschriften `Soll/Haben-Kennzeichen` auf `H` setzen
