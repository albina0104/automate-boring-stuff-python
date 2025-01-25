# Looking Busy
# Nudge your mouse cursor slightly every 10 seconds.

import pyautogui, time

while True:
    time.sleep(10)
    pyautogui.move(100, 0, duration=0.25)    # right
    time.sleep(10)
    pyautogui.move(0, 100, duration=0.25)    # down
    time.sleep(10)
    pyautogui.move(-100, 0, duration=0.25)    # left
    time.sleep(10)
    pyautogui.move(0, -100, duration=0.25)    # up
