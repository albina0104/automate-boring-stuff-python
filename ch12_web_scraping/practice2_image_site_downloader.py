#! /usr/bin/env python3
# image_site_downloader.py - A program that goes to a photo-sharing site,
# searches for a category of photos, and then downloads all the resulting images.
# Search arguments should be provided as command line arguments.

# Note: in theory it should work, but in practice it does not,
# because the website is well protected by Cloudflare -
# it returns 403 to a Python script, while in the browser it works fine.

import sys
import requests
import bs4
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

IMAGE_SITE_URL = 'https://www.pexels.com'
IMAGES_FOLDER = 'downloaded_images'

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': 'en-GB,en;q=0.9',
  'priority': 'u=0, i',
  'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.chdir(IMAGES_FOLDER)

session = requests.Session()
session.headers.update(headers)

search_text = '/search/' + ' '.join(sys.argv[1:]) + '/'
result = session.get(IMAGE_SITE_URL + search_text)
logging.debug('request headers: ' + str(result.request.headers))
logging.debug('response headers: ' + str(result.headers))
logging.debug('response text: ' + result.text)
result.raise_for_status()

results_soup = bs4.BeautifulSoup(result.text, 'html.parser')
photo_page_links = results_soup.select('a[href^="/photo/"]')
for link in photo_page_links:
    photo_page = session.get(IMAGE_SITE_URL + link.attrs['href'])
    photo_page.raise_for_status()
    photo_page_soup = bs4.BeautifulSoup(photo_page.text, 'html.parser')
    img_element = photo_page_soup.select('img[src^="https://images.pexels.com/"]')[0]
    image_url = img_element.attrs['src']
    result = session.get(image_url)
    result.raise_for_status()
    image_file = open(os.path.basename(image_url), 'wb')
    for chunk in result.iter_content(100000):
        image_file.write(chunk)
    image_file.close()

print('Done!')
