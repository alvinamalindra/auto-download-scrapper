import requests
import os
from concurrent.futures import ThreadPoolExecutor

def download_image(url, folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder, url.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def download_images(urls, folder):
    os.makedirs(folder, exist_ok=True)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: download_image(url, folder), urls)

# Example usage
image_urls = [
    "https://kuroyama.id/static/img/314f8a499d41c419f14bdde2e328475a7395e837a0e0abde5d75ed7873aed89e.jpg"
]

download_folder = "downloaded_images"
download_images(image_urls, download_folder)