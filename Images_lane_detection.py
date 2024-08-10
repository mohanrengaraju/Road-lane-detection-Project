import os
import cv2
import numpy as np
import zipfile
import shutil

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_the_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
            if 0.5 < abs(slope) < 2:  # Filter out horizontal and near-vertical lines
                cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=5)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

def process(image):
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (width * 0.1, height),
        (width * 0.4, height * 0.6),
        (width * 0.6, height * 0.6),
        (width * 0.9, height)
    ]
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    canny_image = cv2.Canny(gray_image, 100, 200)
    cropped_image = region_of_interest(canny_image, np.array([region_of_interest_vertices], np.int32))
    lines = cv2.HoughLinesP(cropped_image,
                             rho=1,
                             theta=np.pi / 180,
                             threshold=50,
                             lines=np.array([]),
                             minLineLength=100,
                             maxLineGap=50)
    image_with_lines = draw_the_lines(image, lines)
    return image_with_lines

def process_images_in_zip(zip_file_path, output_zip_path):
    temp_folder = "temp_folder"
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)
    
    output_folder = "processed_images"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(temp_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(temp_folder, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load {filename}")
                continue
            
            processed_image = process(image)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, processed_image)
            print(f"Processed and saved {filename} to {output_folder}")

    shutil.make_archive(output_zip_path.replace('.zip', ''), 'zip', output_folder)
    
    shutil.rmtree(temp_folder)
    shutil.rmtree(output_folder)

# Input and output paths
zip_file_path = r'D:\Mohan\Desktop\next24_intern\Task 1\Road lane detection\images_dataset\road_lane_images.zip'
output_zip_path = r'D:\Mohan\Desktop\next24_intern\Task 1\Road lane detection\processed_lane_detection.zip'

# Process images and save as zip
process_images_in_zip(zip_file_path, output_zip_path)
