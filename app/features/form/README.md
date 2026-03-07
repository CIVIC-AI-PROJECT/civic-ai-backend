# Form Feature

## Purpose
Handles form/document field extraction from uploaded image files.

## Endpoints
- `POST /form/extract`
- `POST /form/generate-application-pdf`
- `POST /form/extract-and-generate-pdf`

## Key Files
- `routes.py` → upload + extraction API
- `services/vision_service.py` → Gemini vision request and JSON parsing
- `services/pdf_service.py` → generated ready-to-print application PDF

## Notes for UI Integration
- Use multipart upload with field name `file`.
- API returns extracted JSON under `data`.
- `POST /form/generate-application-pdf` accepts JSON and returns PDF bytes.
- `POST /form/extract-and-generate-pdf` takes image upload and directly returns PDF.
