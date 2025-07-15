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


#find red colors
def find_red_colors_by_rgb(color_list):
  red_colors = []

  for r, g, b in color_list:
    if r > g and r > b:
      red_colors.append((r, g, b))

  return red_colors

#find deep_red color
def find_deep_red_color(red_colors):
  deep_red = red_colors[0]

  for r, b, g in red_colors:
    if r > deep_red[0]:
      deep_red = r,b,g
  
  return deep_red

red_colors_rgb = find_red_colors_by_rgb(colors_list)
deep_red_color = find_deep_red_color(red_colors_rgb)

print(f"Red colors (by RGB): {red_colors_rgb}")
print(f"Deep red color: {deep_red_color}")


