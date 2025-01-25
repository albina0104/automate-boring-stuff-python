#! /usr/bin/env python3
# command_line_emailer.py
# Takes an email address and string of text on the command line
# and then opens a browser, logs in to my email account and sends an email
# of the string to the provided address.

import sys
import time
import pyinputplus as pyip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email_address_from = 'email.example@mail.ru'
email_address_to = sys.argv[1]
email_text = ' '.join(sys.argv[2:])

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 15)

browser.get('https://mail.ru')

sign_in_button = browser.find_element(By.CSS_SELECTOR, '#mailbox > div.logged-out-one-click > button')
sign_in_button.click()

sign_in_iframe = browser.find_element(By.CLASS_NAME, 'ag-popup__frame__layout__iframe')
browser.switch_to.frame(sign_in_iframe)

email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
email_input.send_keys(email_address_from)
email_input.submit()

password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
password = pyip.inputPassword('Please input the password of your mailbox:\n')

password_input.send_keys(password)
password_input.submit()

browser.switch_to.default_content()
write_email_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Написать письмо')))
write_email_link.click()

recipient_email_input = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div/div/label/div/div/input')))
recipient_email_input.send_keys(email_address_to)

email_area_input = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[4]/div/div/div[2]/div[1]')
email_area_input.send_keys(email_text)

time.sleep(10)

send_button = browser.find_element(By.CSS_SELECTOR, 'button[data-test-id="send"]')
send_button.click()

print('Done!')

