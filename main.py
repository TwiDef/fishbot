import os
import time
import logging
import pyautogui
import random
from PIL import Image, ImageChops
from skimage.metrics import mean_squared_error
from skimage.transform import resize
from skimage.io import imread
from pynput.keyboard import Controller

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)
keyboard = Controller()

screenshots_folder_path = "assets/shots"
diff_folder_path = "assets/diff"
bobber_folder_path = "assets/bobber"
trigger_folder_path = "assets/trigger"

LEFT_FRAME_BORDER = 600
TOP_FRAME_BORDER = 50

def screenshot_frame():
  pyautogui.screenshot(region = (LEFT_FRAME_BORDER, TOP_FRAME_BORDER, 800, 400)).save(screenshots_folder_path + "/s_" + str(random.randint(1, 9999)) + ".png")

def screenshot_bobber(x_coord, y_coord, path, name):
  pyautogui.screenshot(region = (x_coord - 30, y_coord - 30, 60, 60)).save(path + name + ".png")

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

def toFixed(num, digits=0):
  return float(f"{num:.{digits}f}")
  

# game keys binding
fishing_action = "3"
equip_fishing_pole = "r"

def fishing():
  # start programm
  duration = 3
  logging.info(f" capture to focus game window! delay {duration} seconds")

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
  logging.info(" screenshot without bobber has been captured")
  screenshot_frame()

  # start fishing
  keyboard.press(fishing_action)
  time.sleep(0.3)
  keyboard.release(fishing_action) 

  # do screenshot frame with active bobber
  time.sleep(1)
  logging.info(" screenshot with bobber has been captured")
  screenshot_frame()

  # create image list
  image_list = create_image_list(screenshots_folder_path)

  screenshot_1 = Image.open(image_list[0])
  screenshot_2 = Image.open(image_list[1]) 

  res = ImageChops.difference(screenshot_1, screenshot_2)
  logging.info(" difference image has been generated")
  res.save(diff_folder_path + "/result.jpg")

  #get unic colors from diff image
  diff_image_path = diff_folder_path + "/result.jpg"
  unique_colors = get_unic_colors(diff_image_path)
  colors_list = list(unique_colors)

  # find red colors
  red_colors_rgb = find_red_colors_by_rgb(colors_list)

  # find deeper red color
  deep_red_color = find_deep_red_color(red_colors_rgb)

  # find coords by target_color
  coords = find_color_coords(diff_image_path, deep_red_color)

  # generated x an ry coordinates
  try:
    x_coord, y_coord = convert_coords(*coords)
  except Exception:
    print(f"takes 1 positional argument {Exception}")
    #print(f"{x_coord}, {y_coord}")

  # move mouse to dinamic coordinates
  pyautogui.moveTo(x_coord + LEFT_FRAME_BORDER, y_coord + TOP_FRAME_BORDER, duration=0.2)
  #time.sleep(0.3)

  # get mouse position
  x, y = pyautogui.position()

  # catch by trigger
  screenshot_bobber(x, y, bobber_folder_path + "/", "base")

  is_catch = False
  fuse_flag = 55

  while not is_catch:
    # clear trigger screenshots folder
    delete_files_in_folder(trigger_folder_path)

    time.sleep(0.2)
    screenshot_bobber(x,y, trigger_folder_path + "/", "trigger")
      
    # open and convert images      
    img_1 = imread(bobber_folder_path + "/base.png", as_gray=True)
    img_2 = imread(trigger_folder_path + "/trigger.png", as_gray=True)

    img_1_resized = resize(img_1, (512, 512), anti_aliasing=True)
    img_2_resized = resize(img_2, (512, 512), anti_aliasing=True)

    # seek the difference between base image and trigger image (in %)
    mse = mean_squared_error(img_1_resized, img_2_resized)
    max_possible_mse = 1.0 
    similarity_percentage = toFixed((1 - (mse / max_possible_mse)) * 100, 3)
    logging.info(" " + str(similarity_percentage))
    fuse_flag -= 1

    # exit from loop (we have the diffence or waiting too much)
    if similarity_percentage < 99.3 or fuse_flag < 1:
      is_catch = True
      delete_files_in_folder(trigger_folder_path)
      delete_files_in_folder(bobber_folder_path)

  # collect the catch
  logging.info(" collect the catch")
  pyautogui.rightClick()
  time.sleep(1)
  pyautogui.click()

  # remove all screens
  delete_files_in_folder(diff_folder_path)
  delete_files_in_folder(screenshots_folder_path)

# clear working folders
delete_files_in_folder(diff_folder_path)
delete_files_in_folder(screenshots_folder_path)
delete_files_in_folder(trigger_folder_path)
delete_files_in_folder(bobber_folder_path)

# start script 
cast_times = int(input("How many times do you want to cast a fishing? "))
while cast_times > 0:
  fishing()
  cast_times -= 1
