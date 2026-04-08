# PDF Converter

Konvertiert PDFs in Word, PowerPoint, PDF/A oder WebP.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
pip install requests
```

## Verwendung

```bash
python pipeline.py report.pdf word
python pipeline.py contract.pdf pdfa
python pipeline.py slides.pdf powerpoint
python pipeline.py page.pdf webp
```

## Zielformate

| Format | Beschreibung |
|---|---|
| `word` | Microsoft Word (.docx) |
| `powerpoint` | Microsoft PowerPoint (.pptx) |
| `pdfa` | PDF/A (Archivformat) |
| `webp` | WebP-Bild |
