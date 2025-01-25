#! /usr/bin/env python3
# Controlling Your Computer Through Email
# Checks an email account every 15 minutes for instructions you email it
# and executes those instructions automatically.
# If you email the program a (completely legal, not at all piratical) BitTorrent link,
# the program will eventually check its email, find this message, extract the link,
# and then launch qBittorrent to start downloading the file. This way, you can have
# your home computer begin downloads while you’re away, and the (completely legal,
# not at all piratical) download can be finished by the time you return home.

# Crontab entry to run the program every 15 minutes:
# */15 * * * * /path/to/program/practice4_controlling_computer_through_email.py

# Configuring qBittorrent to work correctly with this program:
# 	1. Tools - On Downloads Done - Exit qBittorrent
# 	2. Tools - Preferences - Downloads:
# 		1. untick Display torrent content and some options
# 		2. Default Torrent Management Mode: Automatic

import os
import datetime
import subprocess
import threading
import smtplib
import pyzmail
import logging
import traceback
from imapclient import IMAPClient
from pyzmail.parse import MailPart
from collections import defaultdict
from dotenv import load_dotenv


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='controlling_computer_through_email.log')
logger = logging.getLogger(__name__)

load_dotenv()
SMTP_SERVER_HOST = os.environ.get('SMTP_SERVER_HOST')
SMTP_SERVER_PORT = int(os.environ.get('SMTP_SERVER_PORT'))
SMTP_SERVER_USERNAME = os.environ.get('SMTP_SERVER_USERNAME')
SMTP_SERVER_PASSWORD = os.environ.get('SMTP_SERVER_PASSWORD')
IMAP_SERVER_HOST = os.environ.get('IMAP_SERVER_HOST')
IMAP_SERVER_USERNAME = os.environ.get('IMAP_SERVER_USERNAME')
IMAP_SERVER_PASSWORD = os.environ.get('IMAP_SERVER_PASSWORD')
EMAIL_ADDRESS_FROM = os.environ.get('EMAIL_ADDRESS_FROM')
EMAIL_ADDRESS_TO = os.environ.get('EMAIL_ADDRESS_TO')
EMAIL_SECRET_SUBJECT = os.environ.get('EMAIL_SECRET_SUBJECT')


def login_to_imap_server() -> IMAPClient:
    logger.debug('Logging in to the IMAP server (host: %s, username: %s) ...'
                 % (IMAP_SERVER_HOST, IMAP_SERVER_USERNAME))
    imap_obj = IMAPClient(IMAP_SERVER_HOST, ssl=True)
    imap_obj.login(IMAP_SERVER_USERNAME, IMAP_SERVER_PASSWORD)
    logger.debug('Logging in to the IMAP server - Done.')
    return imap_obj


def logout_from_imap_server(imap_obj: IMAPClient):
    logger.debug('Logging out from the IMAP server...')
    imap_obj.logout()
    logger.debug('Logging out from the IMAP server - Done.')


def get_emails() -> defaultdict:
    yesterday_date = get_yesterday_date()
    imap_obj = login_to_imap_server()
    logger.debug('Getting emails from the IMAP server which arrived since %s...' % yesterday_date)
    imap_obj.select_folder('INBOX', readonly=True)
    uids = imap_obj.search(['SINCE', yesterday_date])
    raw_messages = imap_obj.fetch(uids, ['BODY[]'])
    logout_from_imap_server(imap_obj)
    logger.debug('Getting emails from the IMAP server - Done.')
    return raw_messages


def get_yesterday_date():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)
    return yesterday.strftime('%d-%b-%Y')    # e.g. '01-Jan-2025'


def send_email(message: str):
    logger.debug('Logging in to the SMTP server, sending email message: "%s" ...' % message)
    smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    smtp_obj.ehlo()
    smtp_obj.login(SMTP_SERVER_USERNAME, SMTP_SERVER_PASSWORD)
    smtp_obj.sendmail(EMAIL_ADDRESS_FROM, EMAIL_ADDRESS_TO, message.encode('utf-8'))
    logger.debug('Logging in to the SMTP server, sending email message - Done.')
    smtp_obj.quit()
    logger.debug('Logged out from the SMTP server.')


def delete_email(uid: int):
    logger.debug('Deleting email UID %s from the SMTP server...' % uid)
    imap_obj = login_to_imap_server()
    imap_obj.select_folder('INBOX', readonly=False)
    imap_obj.delete_messages([uid])
    imap_obj.expunge()
    logout_from_imap_server(imap_obj)
    logger.debug('Deleting email from the SMTP server - Done.')


def process_torrent_file_attachment(mailpart: MailPart):
    logger.debug('Processing a torrent file attachment...')
    filename = mailpart.filename
    logger.debug('Getting torrent file: "%s"' % filename)
    torrent_file_content = mailpart.get_payload()
    with open(filename, 'wb') as file:
        file.write(torrent_file_content)
    logger.debug('Saved torrent file "%s" to file.' % filename)

    logger.debug('Opening the file "%s" in qBittorrent...' % filename)
    qbittorrent_process = subprocess.Popen(['qbittorrent', filename])
    logger.debug('Torrent download "%s" has started.' % filename)
    send_email(f'Subject: Torrent download started\nYour torrent "{filename}" downloading has been started!')
    qbittorrent_process.wait()    # Doesn't return until qBittorrent closes.
    logger.debug('Torrent download "%s" has finished.' % filename)
    send_email(f'Subject: Torrent download finished\nYour torrent "{filename}" downloading has been finished!')


def main():
    try:
        logger.info('The program has started.')
        raw_messages = get_emails()
        torrent_processing_threads = []

        for key in raw_messages:
            message = pyzmail.PyzMessage.factory(raw_messages[key][b'BODY[]'])
            email_address_from = message.get_addresses('from')[0][1]
            email_subject = message.get_subject()
            logger.debug('Checking email from %s with subject: "%s"' % (email_address_from, email_subject))
            if not (email_address_from == EMAIL_ADDRESS_FROM and email_subject == EMAIL_SECRET_SUBJECT):
                continue
            mailparts = message.mailparts
            if not mailparts:
                continue
            for mailpart in mailparts:
                if not mailpart.type == 'application/x-bittorrent':
                    continue
                logger.debug('This email has a torrent file attached, it will be processed in a separate thread')
                thread = threading.Thread(target=process_torrent_file_attachment, args=[mailpart])
                torrent_processing_threads.append(thread)
                thread.start()
            delete_email(key)

        for thread in torrent_processing_threads:
            thread.join()
        logger.info('The program has finished.')

    except Exception as e:
        logger.error('Something went wrong, error: %s. %s' % (e, traceback.format_exc()))


if __name__ == '__main__':
    main()
