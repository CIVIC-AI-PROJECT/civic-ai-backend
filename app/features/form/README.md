# Form Feature

## Purpose
Handles form/document field extraction from uploaded image files.

## Endpoints
- `POST /form/extract`

## Key Files
- `routes.py` → upload + extraction API
- `services/vision_service.py` → Gemini vision request and JSON parsing

## Notes for UI Integration
- Use multipart upload with field name `file`.
- API returns extracted JSON under `data`.
