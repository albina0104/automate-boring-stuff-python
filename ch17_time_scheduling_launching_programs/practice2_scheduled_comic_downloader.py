#! /usr/bin/env python3
# Scheduled Web Comic Downloader
# Checks the websites of several web comics and automatically downloads
# the images if the comic was updated since the program’s last visit.
# Copies comics to your desktop so that it is easy to find.

# The crontab entry to schedule it to run once a day at 20:00:
# 0 20 * * * cd /path/to/program && ./practice2_scheduled_comic_downloader.py

import os
import shutil
import requests
import bs4
from urllib.parse import urljoin
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, filename='scheduled_comic_downloader.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ComicDownloader:
    def __init__(self, site_name: str, site_url: str, date_selector: str, img_selector: str,
                 add_site_url_to_img_url: bool = False):
        self.site_name = site_name
        self.site_url = site_url
        self.date_selector = date_selector
        self.img_selector = img_selector
        self.add_site_url_to_img_url = add_site_url_to_img_url

    def download_latest_comic(self):
        comics_dir = self.site_name.lower().replace(' ', '')
        last_comic_date_filename = f'last_comic_date_{comics_dir}.txt'

        os.makedirs(comics_dir, exist_ok=True)

        logger.debug('Checking %s website...' % self.site_name)
        res = requests.get(self.site_url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        last_comic_date = soup.select(self.date_selector)[0].text

        if os.path.exists(last_comic_date_filename):
            logger.debug('Reading previous comic date...')
            with open(last_comic_date_filename, 'r') as file:
                previous_comic_date = file.read()

            if last_comic_date == previous_comic_date:
                logger.debug('The last comic date is the same as the previous time. Nothing to download.')
                return

        with open(last_comic_date_filename, 'w') as file:
            logger.debug('Saving new comic date...')
            file.write(last_comic_date)

        logger.debug('Downloading the new comic image...')
        comic_img_url = soup.select(self.img_selector)[0].get('src')
        if self.add_site_url_to_img_url:
            res = requests.get(urljoin(self.site_url, comic_img_url))
        else:
            res = requests.get(comic_img_url)
        res.raise_for_status()

        img_filename = os.path.basename(comic_img_url)
        img_path = os.path.join(comics_dir, img_filename)
        with open(img_path, 'wb') as image_file:
            for chunk in res.iter_content(100000):
                image_file.write(chunk)
        logger.debug('The new comic image "%s" has been downloaded!' % img_filename)

        shutil.copyfile(img_path, os.path.join(os.path.expanduser('~/Desktop'), img_filename))
        logger.debug('The new comic image has been copied to the desktop.')


if __name__ == '__main__':
    try:
        logger.info('The comic downloader program has started.')

        savagechickens_site = ComicDownloader('Savage Chickens', 'https://www.savagechickens.com',
                                               '.date.time.published', '.entry_content img')
        extraordinary_site = ComicDownloader('Extra Ordinary', 'https://www.exocomics.com',
                                             '.date', '.image-style-main-comic',
                                             True)

        savagechickens_site.download_latest_comic()
        extraordinary_site.download_latest_comic()

        logger.info('The comic downloader program has finished.')
    except Exception as e:
        logger.error('An error occurred while downloading a comic - %s. %s' % (e, traceback.format_exc()))
