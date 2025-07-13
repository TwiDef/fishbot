from PIL import Image, ImageChops

screenshot_1 = Image.open("assets/shots/s_1527.png")
screenshot_2 = Image.open("assets/shots/s_7889.png")

res = ImageChops.difference(screenshot_1, screenshot_2)
res.show()

print(res.getbbox())

res.save("assets/diff/result.jpg")

# rbg(131, 66, 24)
# 671030