import os
import json
import base64
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def extract_fields_from_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": """Extract the following fields from this ID document:

                    - Full Name
                    - Date of Birth
                    - Address
                    - ID Number

                    Return ONLY valid JSON."""},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return {"error": response.json()}

    result = response.json()

    text_output = result["candidates"][0]["content"]["parts"][0]["text"]

    try:
        return json.loads(text_output)
    except Exception:
        return {"raw_output": text_output}
