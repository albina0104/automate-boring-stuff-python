# Using the Clipboard to Read a Text Field

import pyautogui, pyperclip, time

time.sleep(5)
pyautogui.click()
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
print(pyperclip.paste())
