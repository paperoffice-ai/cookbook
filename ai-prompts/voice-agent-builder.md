# Voice Agent Builder

**Tool:** Beliebiges AI-Tool | **Output:** Voice Agent mit TTS + STT

## Prompt

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Create a voice agent that:
1. Takes audio input (Speech-to-Text)
2. Processes the text
3. Generates audio response (Text-to-Speech)

Use POST /voice/tts with:
- voice=Nadja, output_format=mp3, output=url
- Use priority=900 for sync TTS response.
- Bearer token required for all endpoints.
```

## Was du bekommst

Ein Voice-Agent der:
- Audio-Input entgegennimmt und transkribiert
- Den Text verarbeitet (z.B. Fragen beantwortet)
- Eine natürliche Audio-Antwort mit PaperOffice TTS generiert
- Die Stimme `Nadja` für natürlichstes Deutsch verwendet

## Tipps

- `priority=999` für garantiert synchrone TTS-Antwort
- `output=url` liefert eine herunterladbare Audio-URL
- `output=base64` für Inline-Embedding
