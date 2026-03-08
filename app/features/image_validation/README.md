# Image Validation Feature

## Purpose
Validates uploaded image quality before downstream processing.

## Endpoints
- `POST /form/validate-image`

## Key Files
- `routes.py` → validation API endpoint
- `services/blur_checker.py` → blur, glare, and document border quality checks

## Notes for UI Integration
- Use multipart upload with field name `file`.
- API returns `blur`, `glare`, `border`, `is_acceptable`, and `suggestions`.
