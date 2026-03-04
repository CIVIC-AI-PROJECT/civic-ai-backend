from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.features.image_validation.services.blur_checker import check_blur

router = APIRouter(prefix="/form", tags=["Image Validation"])


@router.post("/validate-image")
async def validate_image(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = check_blur(file_path)

    os.remove(file_path)

    return {
        "message": "Image validation complete",
        "data": result
    }
