# Website Image Downloader

A Python script that recursively crawls a website to download images. It provides options for image compression, setting a download limit, and filtering out specific images based on keywords.

## Usage

```bash
python script_name.py <website_url> <compression> [<limit>]
```

- **`<website_url>`**: The starting URL of the website you want to crawl.
- **`<compression>`**: (Optional) Set to "compression" if you want to compress the images.
- **`[<limit>]`**: (Optional) The maximum number of images you want to download.

## Description

This script is designed to help users download images from a website. It starts from the provided URL and recursively visits all linked pages within the same domain, downloading images it finds. The script supports image compression using the PIL library, and users can set a limit on the number of images to download. Additionally, there's a filtering mechanism to skip downloading images with specific keywords in their names.

## Disclaimer

This script is intended for educational purposes and should only be used on websites where you have permission to access and download content. Always respect the terms of service of the website and ensure you're allowed to crawl the website by checking its `robots.txt` file. Misuse may lead to IP bans or legal consequences.
