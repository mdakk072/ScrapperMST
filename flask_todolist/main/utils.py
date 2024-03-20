import os

def load_background_images(static_folder_path):
    """
    Load background images from the specified directory.

    :param static_folder_path: Path to the Flask static directory.
    :return: List of paths to background images.
    """
    backgrounds_dir = os.path.join(static_folder_path, 'background')
    # Generate the path for each background image
    background_images = [os.path.join('background', filename) for filename in os.listdir(backgrounds_dir)]
    return background_images
