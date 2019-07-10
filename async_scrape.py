import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import asyncio
import aiohttp


BASE_URL = "https://apod.nasa.gov/apod/"
MAIN_URL = "https://apod.nasa.gov/apod/archivepix.html"
IMAGE_DIR = "asyncimages"
NUM_OF_IMAGES = 10


async def extract_img_url(url: str) -> str:
    print(f"Downloading page content in {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            print(f"Finished downloading page content {url}")
            soup = BeautifulSoup(content, 'html.parser')
            for img in soup.find_all("a"):
                if img.get("href").startswith("image"):
                    image_url = BASE_URL + img.get("href")
                    print(f"Found {image_url} in {url}")
                    return image_url


async def download_file(img_url: str) -> (str, bytes):
    filename = os.path.basename(urlparse(img_url).path)
    print(f"Begin downloading image {filename}")
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as resp:
            image = await resp.read()
            print(f"Finished Downloading image {filename}")
            return filename, image


async def write_to_file(filename: str, content: bytes) -> None:
    full_path = os.path.join(IMAGE_DIR, filename)
    with open(full_path, 'wb') as f:
        print(f"Begin writing image {full_path}")
        f.write(content)
        print(f"Finished writing image {full_path}")


async def scrape_url(url: str) -> None:
    img_url = await extract_img_url(url)
    if img_url:
        filename, content = await download_file(img_url)
        if filename and content:
            await write_to_file(filename, content)


async def main() -> None:
    page = requests.get(MAIN_URL)
    urls = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all("a"):
            if link.get("href").startswith("ap"):
                urls.append(BASE_URL + link.get("href"))

    tasks = []
    for url in urls[:NUM_OF_IMAGES]:
        tasks.append(scrape_url(url))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Execution time: {elapsed:.2f} seconds")

