from PIL import Image

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
  
image_path = "assets/diff/result.jpg"
target_color = [(131, 24, 66), (131, 23, 65)]

coords = find_color_coords(image_path, target_color)

if isinstance(coords, list):
  if coords:
    print(f"Coords pixel color {target_color}: {coords}")
  else:
    print(f"Pixels {target_color} not found.")
else:
  print(coords)
