# Auto Unsubscriber
# Logs in to your email provider’s IMAP server, downloads all of your emails,
# finds all the unsubscribe links, and automatically opens them in a browser.

import os
import imapclient
import bs4
import pyzmail
import webbrowser
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()
IMAP_SERVER_HOST = os.environ.get('IMAP_SERVER_HOST')
IMAP_SERVER_USERNAME = os.environ.get('IMAP_SERVER_USERNAME')
IMAP_SERVER_PASSWORD = os.environ.get('IMAP_SERVER_PASSWORD')


def get_all_emails() -> defaultdict:
    imap_obj = imapclient.IMAPClient(IMAP_SERVER_HOST, ssl=True)
    imap_obj.login(IMAP_SERVER_USERNAME, IMAP_SERVER_PASSWORD)
    imap_obj.select_folder('INBOX', readonly=True)
    uids = imap_obj.search(['ALL'])
    raw_messages = imap_obj.fetch(uids, ['BODY[]'])
    imap_obj.logout()
    return raw_messages


def open_unsubscribe_links_from_email(soup: bs4.BeautifulSoup):
    unsubscribe_links = soup.find_all(lambda tag: tag.name == 'a' and 'unsubscribe' in tag.text.lower())
    for link in unsubscribe_links:
        print(link['href'])
        webbrowser.open(link['href'])


def main():
    raw_messages = get_all_emails()
    for key in raw_messages:
        message = pyzmail.PyzMessage.factory(raw_messages[key][b'BODY[]'])
        if message.html_part:
            soup = bs4.BeautifulSoup(message.html_part.get_payload().decode(message.html_part.charset),
                                     'html.parser')
            open_unsubscribe_links_from_email(soup)


if __name__ == '__main__':
    main()
