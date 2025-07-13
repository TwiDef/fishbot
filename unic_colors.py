from PIL import Image
import colorsys

#get unic colors
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
  
image_path = "assets/diff/result.jpg"
unique_colors = get_unic_colors(image_path)
colors_list = list(unique_colors)

#sorting colors
def sort_rgb_by_hue(rgb_list):
  normalized_rgb_list = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in rgb_list]

  sorted_normalized_rgb = sorted(normalized_rgb_list, key=lambda rgb: colorsys.rgb_to_hsv(*rgb)[0])

  sorted_rgb_list = [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in sorted_normalized_rgb]
  return sorted_rgb_list

sorted_colors = sort_rgb_by_hue(colors_list)
print(sorted_colors)

""" if isinstance(unique_colors, set):
    print("Unic colors in image")
    for color in unique_colors:
      print(color)
else:
  print(unique_colors) """

