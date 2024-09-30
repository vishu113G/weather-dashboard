import os
import uuid

from PIL import Image, ImageChops


def compare_images(img1_path, img2_path):
    current_dir = os.path.dirname(__file__)  # Directory where the test script is located
    img2_path = os.path.join(current_dir, '..', img2_path)

    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    diff = ImageChops.difference(img1, img2)

    if diff.getbbox() is None:
        print("The images are the same")
        return True
    else:
        diff.show()  # Opens the difference image visually
        print("The images are different")
        return False


def delete_test_screenshots():
    # Define the folder to scan
    folder_path = "./screenshots"

    # Loop through all files in the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a .png file and contains "test" in its name
            if file.endswith(".png") and "test" in file:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


def generate_unique_id():
    # Generates a 6-digit random UUID
    random_uuid = str(uuid.uuid4().int)[:6]
    return random_uuid
