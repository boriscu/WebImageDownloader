import os
import sys
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from urllib.parse import urlparse, urljoin

SAVE_PATH = "downloaded_images"
visited_urls = set()
downloaded_images_count = 0

FILTER_KEYWORDS = [
    "twitter",
    "vimeo",
    "youtube",
    "linkedin",
    "instagram",
    "facebook",
    "maxi",
    "univer",
    "temp",
    "dis",
    "roda",
    "aksa",
    "petcentar",
    "petspot",
    "lidl",
    "shoppster",
    "gomex",
    "idea",
    "kategorija",
    "logo",
    "neoplanta",
]


def compress_image(img_path):
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]
    file_ext = os.path.splitext(img_path)[1].lower()

    if file_ext not in valid_image_extensions:
        print(f"Skipping compression for {img_path} due to unsupported format.")
        return

    with Image.open(img_path) as img:
        img.save(img_path, quality=20, optimize=True)


def sanitize_filename(filename):
    file_root, file_ext = os.path.splitext(filename)
    s = re.sub(r"[^\w\s-]", "", file_root).strip().lower()
    s = re.sub(r"[-\s]+", "_", s)

    return s + file_ext


def download_images_from_url(url, save_path, compression, max_images):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    global visited_urls
    if url in visited_urls:
        return
    visited_urls.add(url)

    global downloaded_images_count
    if downloaded_images_count >= max_images:
        print(f"Reached the limit of {max_images} images. Exiting.")
        return

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    img_tags = soup.find_all("img")

    for img_tag in img_tags:
        if downloaded_images_count >= max_images:
            print(f"Reached the limit of {max_images} images. Exiting.")
            return

        img_url = img_tag["src"]

        if not img_url:
            print("Skipping due to empty src attribute.")
            continue
        if not img_url.startswith(("http://", "https://")):
            img_url = urljoin(url, img_url)
        if not img_url.startswith(("http://", "https://")):
            print(f"Skipping non-absolute URL: {img_url}")
            continue

        img_name = sanitize_filename(os.path.basename(img_url))
        if any(keyword in img_name.lower() for keyword in FILTER_KEYWORDS):
            continue

        img_path = os.path.join(save_path, img_name)

        img_data = requests.get(img_url).content
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)

        print(f"Downloaded {img_name}")

        if compression == "compression":
            compress_image(img_path)

    for a_tag in soup.find_all("a", href=True):
        next_url = a_tag["href"]
        next_url = urljoin(url, next_url)
        domain = urlparse(url).netloc
        if urlparse(next_url).netloc == domain:
            download_images_from_url(next_url, save_path, compression, max_images)


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print("Usage: python script_name.py <website_url> <compression>")
        sys.exit(1)

    website_url = sys.argv[1]
    compression = sys.argv[2].lower()
    max_images = int(sys.argv[3]) if len(sys.argv) == 4 else float("inf")
    download_images_from_url(website_url, SAVE_PATH, compression, max_images)
