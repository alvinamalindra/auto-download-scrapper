import csv
import requests
import os
from PIL import Image
import pytesseract
import re

# Step 1: Read the CSV file
def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row['proof_filename'] for row in reader]

# Step 2: Download images
def download_image(image_id, url_template, save_dir):
    url = url_template.format(image_id)
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(save_dir, image_id)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {image_id}")
    else:
        print(f"Failed to download: {image_id}")

# Step 3: Extract text from image using OCR
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Step 4: Process text to get transaction number
def get_transaction_number(text):
    # This is a placeholder regex. Adjust it based on the actual format of your transaction numbers
    match = re.search(r'\b\d{10,}\b', text)
    return match.group(0) if match else None

# Main function
def main():
    csv_file = 'transaction_proofs.csv'  # Update this to your CSV file name
    url_template = 'https://kuroyama.id/static/img/{}'
    save_dir = 'downloaded_transaction_proofs'
    
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Read image IDs from CSV
    image_ids = read_csv(csv_file)
    
    # Download images and process them
    for image_id in image_ids:
        # Download image
        download_image(image_id, url_template, save_dir)
        
        # Extract text from image
        image_path = os.path.join(save_dir, image_id)
        text = extract_text_from_image(image_path)
        
        # Get transaction number
        transaction_number = get_transaction_number(text)
        
        if transaction_number:
            print(f"Image: {image_id}, Transaction Number: {transaction_number}")
        else:
            print(f"Image: {image_id}, No transaction number found")

if __name__ == "__main__":
    main()