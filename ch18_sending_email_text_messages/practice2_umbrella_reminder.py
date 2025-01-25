#! /usr/bin/env python3
# umbrella_reminder.py
# Checks whether it’s raining before you wake up in the morning.
# If so, texts you a reminder to pack an umbrella before leaving the house.

# Note 1. Ollama needs to be installed on the computer for this program to work.
# Note 2. Crontab entry to schedule it to run every morning at 7:00:
# 0 7 * * * /path/to/program/practice2_umbrella_reminder.py

import os
import requests
import bs4
import smtplib
import logging
import traceback
from dotenv import load_dotenv
from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel


logging.basicConfig(level=logging.DEBUG, filename='umbrella_reminder.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

WEATHER_SITE_URL = 'https://forecast.weather.gov/MapClick.php?lat=42.93708397900008&lon=-75.61070144699994'  # New York

load_dotenv()
SMTP_SERVER_HOST = os.environ.get('SMTP_SERVER_HOST')
SMTP_SERVER_PORT = int(os.environ.get('SMTP_SERVER_PORT'))
SMTP_SERVER_USERNAME = os.environ.get('SMTP_SERVER_USERNAME')
SMTP_SERVER_PASSWORD = os.environ.get('SMTP_SERVER_PASSWORD')
EMAIL_ADDRESS_FROM = os.environ.get('EMAIL_ADDRESS_FROM')
EMAIL_ADDRESS_TO = os.environ.get('EMAIL_ADDRESS_TO')


class WeatherForecast(BaseModel):
    is_raining: bool


def get_today_forecast() -> str:
    try:
        logger.debug('Getting weather forecast from a weather site...')
        response = requests.get(WEATHER_SITE_URL)
        response.raise_for_status()

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        today_forecast = soup.select('#detailed-forecast-body > div:nth-child(1) > div.col-sm-10.forecast-text')[
            0].getText()

        logger.debug("Got today's forecast: %s" % today_forecast)
        return today_forecast
    except Exception as e:
        logger.error('Error fetching weather data: %s. %s' % (e, traceback.format_exc()))
        return ''


def is_raining_today(today_forecast: str) -> bool:
    logger.debug("LLM will determine if it's raining today...")
    prompt = (f'Here is the weather forecast for today: "{today_forecast}" '
              'Please respond with one word "yes" or "no" to the question: '
              'is there a chance of rain today? Do not include any other words '
              'in your response other than "yes" or "no".'
              'Do not use any punctuation marks in your response.')
    response: ChatResponse = chat(
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        model='gemma:2b',
        format=WeatherForecast.model_json_schema()
    )
    logger.debug('Got response from LLM: %s' % response)
    return WeatherForecast.model_validate_json(response.message.content).is_raining


def send_email(email_text):
    try:
        logger.debug('Sending email with the content: "%s"' % email_text)
        smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        smtp_obj.ehlo()
        smtp_obj.login(SMTP_SERVER_USERNAME, SMTP_SERVER_PASSWORD)
        smtp_obj.sendmail(EMAIL_ADDRESS_FROM, EMAIL_ADDRESS_TO, email_text)
        smtp_obj.quit()
        logger.debug('Email has been sent.')
    except Exception as e:
        logger.error('Error sending email: %s. %s' % (e, traceback.format_exc()))


def main():
    logger.info('The Umbrella Reminder program has started.')
    try:
        today_forecast = get_today_forecast()
        if today_forecast and is_raining_today(today_forecast):
            logger.debug("It's raining, an email reminder will be sent...")
            email_text = ('Subject: Umbrella Reminder\n\nThere is a chance of rain today. '
                          'Please grab an umbrella before leaving the house!')
            send_email(email_text)
    except Exception as e:
        logger.error('An error occurred: %s. %s' % (e, traceback.format_exc()))
    logger.info('The Umbrella Reminder program has finished.')


if __name__ == '__main__':
    main()
