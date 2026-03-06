from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.features.image_validation.services.blur_checker import check_blur
from app.features.form.services.vision_service import extract_fields_from_image

router = APIRouter(prefix="/form", tags=["Form"])


@router.post("/extract")
async def extract_form(file: UploadFile = File(...)):

    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    blur_result = check_blur(file_path)

    if blur_result["is_blurry"]:
        os.remove(file_path)
        return {
            "error": "Image is blurry. Please retake.",
            "blur_score": blur_result["blur_score"]
        }

    extracted_data = extract_fields_from_image(file_path)

    os.remove(file_path)

    return {
        "message": "Extraction successful",
        "data": extracted_data
    }
