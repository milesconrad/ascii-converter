from sys import argv, exit
from PIL import Image, UnidentifiedImageError

if len(argv) != 2:
    print("Please provide an image you'd like to process")
    exit()

image = None
try:
    image = Image.open(argv[1])
except FileNotFoundError:
    print("Sorry, that file doesn't seem to exist")
    exit()
except UnidentifiedImageError:
    print("Sorry, the file you provided is not an image")
    exit()

if image.format == "GIF":
    image = image.convert("RGB")
pixels = image.load()
width, height = image.size

# makes image grayscale
for i in range(height):
    for j in range(width):
        pixels[j, i] = int(round(sum(pixels[j, i]) / float(len(pixels[j, i]))))

# brightness_index helps us convert an RGB byte to a number 0-12, which we can convert to a corresponding character
# pixelate factor determines how many pixels we skip over when writing to the final string
pixels_as_chars = []
char_convert = [" ", ".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"]
brightness_index = 255 / (len(char_convert) - 1)
pixelate_factor = 0
if width >= height:
    pixelate_factor = width / 100
elif width < height:
    pixelate_factor = height / 100

pixel_value = 0
for i in range(int(height / pixelate_factor)):
    pixels_as_chars.append(list())

    for j in range(int(width / pixelate_factor)):
        # we get the first index because the pixel object is a tuple of RGB values
        pixel_value = pixels[j * pixelate_factor, i * pixelate_factor][0]
        pixels_as_chars[i].append(char_convert[round(pixel_value / brightness_index)])
        
line = ""
for i in range(len(pixels_as_chars)):
    for j in range(len(pixels_as_chars[i])):
        line += str(pixels_as_chars[i][j])
        line += "  "
    print(line)
    line = ""
