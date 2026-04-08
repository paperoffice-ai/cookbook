# Voice Documentation

Konvertiert Dokumente in Audio — perfekt für Barrierefreiheit, Podcasts aus Berichten, oder Audio-Handbücher.

## Workflow

```
1. Dokument OCR (Text extrahieren)
2. Text in Abschnitte teilen (max 5000 Zeichen)
3. TTS für jeden Abschnitt
4. Audio-URLs ausgeben
```

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
pip install requests
```

## Verwendung

```bash
python pipeline.py handbuch.pdf           # Stimme: Nadja (Standard)
python pipeline.py bericht.pdf Thomas     # Stimme: Thomas
```

## Deutsche Stimmen

| Stimme | Beschreibung |
|---|---|
| `Nadja` | Weiblich, natürlich (empfohlen) |
| `Thomas` | Männlich, professionell |
| `Anna` | Weiblich, warm |
| `Hans` | Männlich, neutral |
