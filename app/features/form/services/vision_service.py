import os
import json
import base64
import mimetypes
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def extract_fields_from_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    if not GEMINI_API_KEY:
        return {
            "success": False,
            "error": "GEMINI_API_KEY is not configured"
        }

    mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": """Extract the following fields from this ID document or handwritten form note:

                    - Full Name
                    - Date of Birth
                    - Address
                    - ID Number
                    - Document Type

                    Return ONLY valid JSON with keys:
                    full_name, date_of_birth, address, id_number, document_type."""},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as exc:
        return {
            "success": False,
            "error": f"Vision API request failed: {str(exc)}"
        }

    if response.status_code != 200:
        try:
            details = response.json()
        except Exception:
            details = response.text

        return {
            "success": False,
            "error": "Vision API returned non-200 response",
            "details": details
        }

    result = response.json()

    try:
        text_output = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return {
            "success": False,
            "error": "Unexpected response format from Vision API",
            "details": result
        }

    try:
        parsed = json.loads(text_output)
        return {
            "success": True,
            "data": parsed
        }
    except Exception:
        return {
            "success": False,
            "error": "Model output was not valid JSON",
            "raw_output": text_output
        }
