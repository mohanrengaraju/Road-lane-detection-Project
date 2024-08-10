import os
import zipfile

def create_zip_of_images(input_folder, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, input_folder))
    print(f"Created zip file: {zip_file_path}")

# Define the input folder and output zip file path
input_folder = r'D:\Mohan\Desktop\next24_intern\Task 1\Road lane detection\images_dataset'
zip_file_path = os.path.join(input_folder, 'road_lane_images.zip')

# Create a zip file of the images
create_zip_of_images(input_folder, zip_file_path)
