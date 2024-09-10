import os
import csv
from PIL import Image
import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification

# Set up the model and feature extractor
model_name = "AshleyPoole/benedicamus-v1"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# Set up paths
manuscript_dir = 'data/manuscript'
output_dir = 'data/inference'
os.makedirs(output_dir, exist_ok=True)

# Prepare the CSV file
csv_path = os.path.join(output_dir, 'inference_results.csv')
csv_header = ['image_name', 'has_benedicamus_probability', 'does_not_have_benedicamus_probability']

# Function to perform inference on a single image
def infer_image(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    has_benedicamus_prob = probabilities[0][1].item()  # Assuming index 1 is for "has_benedicamus"
    does_not_have_benedicamus_prob = probabilities[0][0].item() 
    
    return has_benedicamus_prob, does_not_have_benedicamus_prob

# Main inference loop
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_header)
    
    for image_name in os.listdir(manuscript_dir):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(manuscript_dir, image_name)
            probability_yes, probability_no = infer_image(image_path)
            writer.writerow([image_name, probability_yes, probability_no])
            print(f"Processed {image_name}: {probability_yes:.4f}")

print(f"Inference completed. Results saved to {csv_path}")
