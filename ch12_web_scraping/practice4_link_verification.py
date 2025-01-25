# link_verification.py - given the URL of a web page, will attempt to download
# every linked page on the page. The program should flag any pages that have
# a 404 “Not Found” status code and print them out as broken links.

import requests
import bs4
import traceback
from urllib.parse import urlparse, urljoin

URL = 'https://automatetheboringstuff.com/2e/chapter12/'

def is_valid_url(url):
    try:
        res = urlparse(url)
        return all([res.scheme, res.netloc])
    except:
        return False


try:
    result = requests.get(URL)
    result.raise_for_status()

    result_soup = bs4.BeautifulSoup(result.text, 'html.parser')
    link_elems = result_soup.select('a')

    visited_urls = set()

    for link_elem in link_elems:
        try:
            link = link_elem.attrs.get('href')
            if not link:
                continue
            link = urljoin(URL, link)  # to make absolute URL out of relative

            if link in visited_urls:
                continue

            visited_urls.add(link)

            if not is_valid_url(link):
                continue

            page = requests.get(link)
            page.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print('Unreachable page: ' + link + '. HTTP status code: ' + str(page.status_code))
        except Exception as e:
            print('An error occurred: ' + str(e))
            print(traceback.format_exc())

    print('Done!')

except Exception as e:
    print(f'An error occurred while processing the main page: {e}')
    print(traceback.format_exc())
