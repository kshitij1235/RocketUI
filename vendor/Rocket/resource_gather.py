import os

def get_resource_images(image_name):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the project root directory
    project_root = os.path.normpath(os.path.join(current_directory, '..', '..'))

    # Construct the path to the image file relative to the project root
    image_path = os.path.join(project_root, 'resources', 'images', image_name)

    print(f"Looking for image at: {image_path}")  # Debugging: Print the image path

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image '{image_name}' not found at path: {image_path}")

    return image_path
