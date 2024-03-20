import os

def get_profile_images(static_folder_path):
    """
    Generates a list of filenames for profile images stored in static/profile_pics/.

    :param static_folder_path: Path to the Flask static directory.
    :return: Sorted list of profile image filenames.
    """
    profile_pics_dir = os.path.join(static_folder_path, 'profile_pics')
    profile_images = [filename for filename in os.listdir(profile_pics_dir) if os.path.isfile(os.path.join(profile_pics_dir, filename))]
    profile_images.sort()  # Sort the filenames
    return profile_images
