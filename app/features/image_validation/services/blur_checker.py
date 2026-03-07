import cv2
import numpy as np


def check_blur(image_path, threshold=800):

    image = cv2.imread(image_path)

    if image is None:
        return {
            "error": "Invalid image file"
        }

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    is_blurry = laplacian_var < threshold

    return {
        "blur_score": float(laplacian_var),
        "is_blurry": bool(is_blurry),
        "threshold_used": threshold
    }


def check_glare(image: np.ndarray, glare_threshold: int = 245, max_glare_ratio: float = 0.12):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bright_pixels = np.sum(gray >= glare_threshold)
    total_pixels = gray.size
    ratio = bright_pixels / max(total_pixels, 1)
    return {
        "glare_ratio": float(ratio),
        "has_glare": bool(ratio > max_glare_ratio),
        "max_glare_ratio": max_glare_ratio,
        "glare_threshold": glare_threshold,
    }


def check_document_border(image: np.ndarray, min_area_ratio: float = 0.40, margin_px: int = 8):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    h, w = gray.shape[:2]
    image_area = float(h * w)
    if not contours:
        return {
            "document_detected": False,
            "area_ratio": 0.0,
            "is_cut_off": True,
            "reason": "No document contour found",
        }

    largest = max(contours, key=cv2.contourArea)
    area = float(cv2.contourArea(largest))
    x, y, cw, ch = cv2.boundingRect(largest)
    area_ratio = area / max(image_area, 1.0)

    touches_edge = (
        x <= margin_px
        or y <= margin_px
        or (x + cw) >= (w - margin_px)
        or (y + ch) >= (h - margin_px)
    )

    return {
        "document_detected": bool(area_ratio >= min_area_ratio),
        "area_ratio": float(area_ratio),
        "is_cut_off": bool(touches_edge or area_ratio < min_area_ratio),
        "bounding_box": {"x": int(x), "y": int(y), "width": int(cw), "height": int(ch)},
        "min_area_ratio": min_area_ratio,
    }


def run_quality_checks(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Invalid image file"}

    blur = check_blur(image_path)
    glare = check_glare(image)
    border = check_document_border(image)

    suggestions = []
    if blur.get("is_blurry"):
        suggestions.append("Retake image with steady hands and better focus")
    if glare.get("has_glare"):
        suggestions.append("Avoid flash and tilt document to reduce reflections")
    if border.get("is_cut_off"):
        suggestions.append("Capture the full document within frame margins")

    return {
        "blur": blur,
        "glare": glare,
        "border": border,
        "is_acceptable": len(suggestions) == 0,
        "suggestions": suggestions,
    }
