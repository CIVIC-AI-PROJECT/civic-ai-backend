from fastapi import APIRouter, UploadFile, File
from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import shutil
import os

from app.features.image_validation.services.blur_checker import check_blur
from app.features.form.services.vision_service import extract_fields_from_image
from app.features.form.services.pdf_service import generate_application_pdf
from app.models.form_model import GeneratePdfRequest

router = APIRouter(prefix="/form", tags=["Form"])

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/extract")
async def extract_form(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

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

    if not extracted_data.get("success"):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Form extraction failed",
                "error": extracted_data.get("error"),
                "details": extracted_data.get("details") or extracted_data.get("raw_output")
            },
        )

    return {
        "message": "Extraction successful",
        "data": extracted_data["data"]
    }


@router.post("/generate-application-pdf")
def generate_pdf(payload: GeneratePdfRequest):
    pdf_path = generate_application_pdf(
        fields=payload.fields.model_dump(),
        output_dir=UPLOAD_FOLDER,
        application_title=payload.application_title,
        scheme_name=payload.scheme_name,
        language_hint=payload.language_hint,
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
        background=BackgroundTask(lambda: os.path.exists(pdf_path) and os.remove(pdf_path)),
    )


@router.post("/extract-and-generate-pdf")
async def extract_and_generate_pdf(
    file: UploadFile = File(...),
):
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    blur_result = check_blur(file_path)
    if blur_result.get("is_blurry"):
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Image is blurry. Please retake.",
                "blur_score": blur_result.get("blur_score"),
            },
        )

    extracted_data = extract_fields_from_image(file_path)
    os.remove(file_path)

    if not extracted_data.get("success"):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Extraction failed before PDF generation",
                "error": extracted_data.get("error"),
                "details": extracted_data.get("details") or extracted_data.get("raw_output"),
            },
        )

    pdf_path = generate_application_pdf(
        fields=extracted_data["data"],
        output_dir=UPLOAD_FOLDER,
        application_title="Government Scheme Application",
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
        background=BackgroundTask(lambda: os.path.exists(pdf_path) and os.remove(pdf_path)),
    )
