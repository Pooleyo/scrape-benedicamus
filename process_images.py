import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def process_image(input_path, output_path):
    # Read the image
    img = cv2.imread(input_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Denoise the image
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    # Convert back to PIL Image for further processing
    pil_img = Image.fromarray(denoised)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(pil_img)
    enhanced_img = enhancer.enhance(2.0)  # Increase contrast by a factor of 2
    
    # Resize the image to a standard size (e.g., 224x224 for many CNN architectures)
    resized_img = enhanced_img.resize((224, 224), Image.LANCZOS)
    
    # Save the processed image
    resized_img.save(output_path)

def process_all_images():
    input_dir = 'data/manuscript'
    output_dir = 'data/processed_images'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            process_image(input_path, output_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    process_all_images()
    print("Image processing completed.")
