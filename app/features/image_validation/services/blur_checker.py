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
