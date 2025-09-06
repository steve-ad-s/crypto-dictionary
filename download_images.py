import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

# Ensure the directory exists
directory = 'candlesticks_images_missing'
if not os.path.exists(directory):
    os.makedirs(directory)

# List of candlestick patterns
patterns = [
    "Rising Three Methods", "Falling Three Methods", "Stick Sandwich",
    "On-Neck Pattern", "In-Neck Pattern", "Thrusting Pattern",
    "Bullish Belt Hold", "Bearish Belt Hold", "Unique Three River Bottom",
    "Three Stars in the South", "Concealing Baby Swallow", "Ladder Bottom",
    "Advance Block", "Deliberation Pattern", "High Wave Candle"
]

# Function to download an image
def download_image(url, folder, filename):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.save(os.path.join(folder, filename))
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

# Loop through each pattern
for pattern in patterns:
    query = pattern.replace(' ', '+') + "+candlestick+pattern"
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    # Download the first image
    if img_tags:
        img_url = img_tags[1]['src'] # Changed from 0 to 1 to skip google logo
        if not img_url.startswith('http'):
            img_url = urljoin(url, img_url)
        filename = f"{pattern.replace(' ', '_')}.png"
        download_image(img_url, directory, filename)
    else:
        print(f"No images found for {pattern}")
