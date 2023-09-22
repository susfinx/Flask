import os
import requests
import concurrent.futures
import asyncio
import aiohttp
import time
import argparse

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(url)
            with open(filename, 'wb') as file:
                file.write(response.content)
            return f"Downloaded {filename}"
        else:
            return f"Failed to download {url}"
    except Exception as e:
        return f"Error downloading {url}: {str(e)}"

async def async_download_image(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.basename(url)
                with open(filename, 'wb') as file:
                    file.write(await response.read())
                return f"Downloaded {filename}"
            else:
                return f"Failed to download {url}"
    except Exception as e:
        return f"Error downloading {url}: {str(e)}"

def multithreaded_download(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    return results

def multiprocessing_download(urls):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    return results

async def async_download(urls):
    ssl_context = None
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = [async_download_image(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from URLs")
    parser.add_argument("urls", nargs="+", help="List of image URLs to download")
    args = parser.parse_args()

    start_time = time.time()

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(async_download(args.urls))

    for result in results:
        print(result)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
