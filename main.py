# use Fishing => mouseover bobber => delay 6s => click G(interact) => click mouse_1 => delay 5s => loop
import pyautogui
import random
from time import sleep

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

[width, height] = (pyautogui.size())

print(width, height)

def shot_display():
  pyautogui.screenshot(region = (600, 50, 800, 400)).save("assets/shots/s_" + str(random.randint(1, 9999)) + ".png")
  print("screenshot captured")
  sleep(1)
shot_display()

