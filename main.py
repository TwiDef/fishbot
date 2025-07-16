from PIL import Image, ImageChops
import os
import time
import logging
import pyautogui
import random
from pynput.keyboard import Controller

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
keyboard = Controller()

screenshots_folder_path = "assets/shots"
diff_folder_path = "assets/diff"

LEFT_FRAME_BORDER = 600
TOP_FRAME_BORDER = 50

def screenshot_frame():
  pyautogui.screenshot(region = (LEFT_FRAME_BORDER, TOP_FRAME_BORDER, 800, 400)).save("assets/shots/s_" + str(random.randint(1, 9999)) + ".png")

def create_image_list(dir_path):
  image_list = []

  for filename in os.listdir(dir_path):
    if filename.lower().endswith("png"):
      image_list.append(os.path.join(dir_path, filename))
  return image_list

def get_unic_colors(image_path):

  try:
    img = Image.open(image_path)
    img = img.convert("RGB") 
    width, height = img.size
    colors = set()

    for x in range(width):
      for y in range(height):
        r, g, b = img.getpixel((x, y))
        colors.add((r, g, b))

    return colors
  except FileNotFoundError:
    return f"Error: file not found {image_path}"
  except Exception as e:
    return f"Error with file processing {e}"
  
def find_red_colors_by_rgb(color_list):
  red_colors = []

  for r, g, b in color_list:
    if r > g and r > b:
      red_colors.append((r, g, b))

  return red_colors

def find_deep_red_color(red_colors):
  deep_red = red_colors[0]

  for r, b, g in red_colors:
    if r > deep_red[0]:
      deep_red = r,b,g
  
  return deep_red

def find_color_coords(image_path, target_color):
  try:
    img = Image.open(image_path)
    width, height = img.size
    coords = []

    for y in range(height):
      for x in range(width):
        pixel_color = img.getpixel((x, y))
        if pixel_color == target_color:
          coords.append((x, y))
    return coords
  except FileNotFoundError:
    return "Error: file not found"
  except Exception:
    return f"Error: {Exception}"      
  
def convert_coords(coords):
  tuple_coords = coords
  return tuple_coords

def delete_files_in_folder(folder_path):
  for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
      if os.path.isfile(file_path):
        os.remove(file_path)
    except Exception:
      print(f'Ошибка при удалении файла {file_path}. {Exception}')
  

# game keys binding
fishing_action = "3"
equip_fishing_pole = "r"

def fishing():
  # start programm
  duration = 6
  logging.info("capture to focus game window! delay 10 seconds")

  while duration > 0:
    logging.info(" " + str(duration) + " seconds remaining...")
    time.sleep(1)
    duration -= 1

  # equip fishing pole 
  keyboard.press(equip_fishing_pole)
  time.sleep(0.3)
  keyboard.release(equip_fishing_pole)

  # do screenshot frame without bobber
  time.sleep(1)
  logging.info("screenshot without bobber has been captured")
  screenshot_frame()

  # start fishing
  keyboard.press(fishing_action)
  time.sleep(0.3)
  keyboard.release(fishing_action) 

  # do screenshot frame with active bobber
  time.sleep(1)
  logging.info("screenshot with bobber has been captured")
  screenshot_frame()

  # create image list
  image_list = create_image_list("assets/shots")

  screenshot_1 = Image.open(image_list[0])
  screenshot_2 = Image.open(image_list[1]) 

  res = ImageChops.difference(screenshot_1, screenshot_2)
  logging.info("difference image has been generated")
  res.save("assets/diff/result.jpg")

  #get unic colors from diff image
  diff_image_path = "assets/diff/result.jpg"
  unique_colors = get_unic_colors(diff_image_path)
  colors_list = list(unique_colors)

  # find red colors
  red_colors_rgb = find_red_colors_by_rgb(colors_list)

  # find deeper red color
  deep_red_color = find_deep_red_color(red_colors_rgb)

  # find coords by target_color
  coords = find_color_coords(diff_image_path, deep_red_color)

  # generated x an dy coordinates
  x_coord, y_coord = convert_coords(*coords)

  # move mouse to dinamic coordinates
  pyautogui.moveTo(x_coord + LEFT_FRAME_BORDER, y_coord + TOP_FRAME_BORDER, duration=0.5)
  time.sleep(6.5)

  # collect the catch
  logging.info("collect the catch")
  pyautogui.rightClick()
  time.sleep(1)
  pyautogui.click()

  # remove all screens
  delete_files_in_folder(diff_folder_path)
  delete_files_in_folder(screenshots_folder_path)

  duration = 10

i = 50
while i > 1:
  fishing()
  i -= 1