import os

from vendor.Rocket.Log import log

_BASE_IMAGE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "resources", "images")
)

_ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def get_resource_image(image_name: str) -> str:
    if not image_name:
        raise ValueError("Image name cannot be empty")

    _, ext = os.path.splitext(image_name)
    if ext.lower() not in _ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid image extension: {ext}")

    image_path = os.path.abspath(os.path.join(_BASE_IMAGE_DIR, image_name))

    # Prevent directory traversal
    if not image_path.startswith(_BASE_IMAGE_DIR + os.sep):
        raise ValueError("Invalid image path")

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_name}")

    log(f"resource loaded: {image_name}")

    return image_path
