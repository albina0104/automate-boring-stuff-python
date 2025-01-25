# 2048.py - Opens the 2048 game in the browser and keeps sending
# up, right, down, and left keystrokes to automatically play the game.
# You can actually get a fairly high score like this.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('https://play2048.co/')

html_elem = browser.find_element(By.TAG_NAME, 'html')

while True:
    html_elem.send_keys(Keys.UP)
    html_elem.send_keys(Keys.RIGHT)
    html_elem.send_keys(Keys.DOWN)
    html_elem.send_keys(Keys.LEFT)
