# Instant Messenger Bot
# Sends a message in WhatsApp to the list of contacts.

import pyautogui, time

CONTACT_NAMES = ['Mom', 'Name Surname']
MESSAGE = ("My automation program automatically sent you a message."
           " Sorry for disturbing if it was sent to you accidentally.")

pyautogui.PAUSE = 2
time.sleep(5)

for name in CONTACT_NAMES:
    try:
        pyautogui.click('whatsapp_search_field.png')
    except Exception as e:
        print('WhatsApp search field has not been found.')
        exit(1)

    pyautogui.write(name, 0.25)
    pyautogui.press('enter')
    pyautogui.write(MESSAGE, 0.25)
    pyautogui.press('enter')
