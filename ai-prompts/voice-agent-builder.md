# Voice Agent Builder

**Tool:** Any AI Tool | **Output:** Voice Agent with TTS + STT

## Prompt

```
Read this API guide first, completely:
https://api.paperoffice.ai/latest/docs/llms.txt
Use the Postman collection at https://api.paperoffice.ai/latest/docs/postman only for exact request and response samples.

Create a voice agent that:
1. Takes audio input (Speech-to-Text)
2. Processes the text
3. Generates audio response (Text-to-Speech)

Use POST /job/add/paperoffice_voice___tts with:
- voice=Nadja, language=de, output_format=mp3, output=url
- language is REQUIRED (e.g. de, en, es, fr)
- Use processing_lane=instant for sync TTS response.
- For STT use POST /job/add/paperoffice_voice___stt with file_1 parameter.
- Bearer token required for all endpoints.
```

## What you get

A voice agent that:
- Accepts audio input and transcribes it
- Processes the text (e.g. answers questions)
- Generates a natural audio response with PaperOffice TTS
- Uses the `Nadja` voice for the most natural German

## Tips

- `processing_lane=no_sla` for guaranteed synchronous TTS response
- `output=url` returns a downloadable audio URL
- `output=base64` for inline embedding
