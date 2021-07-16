from PIL import Image
import os


class ToAscii:
    def __init__(self, ASCII_CHARS=["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]):
        self.ASCII_CHARS = ASCII_CHARS

    def main(self, img):
        
        image = Image.open(img)
        image = image.convert('L')
        image = self.resize(image)
        ascii_img = ''
        ascii_str = self.pixel_to_ascii(image)
        img_width = image.width
        for i in range(0, len(ascii_str), img_width):
            ascii_img += ascii_str[i:i+img_width] + "\n"
        os.remove(img)
        return ascii_img

    def resize(self, image, new_width=100):
        #width, height = image.size
        #new_height = int(new_width * height / width)

        return image.resize((new_width, new_width))

    def pixel_to_ascii(self, image):
        pixels = image.getdata()
        ascii_str = ""

        for pixel in pixels:
            ascii_str += self.ASCII_CHARS[pixel//25]

        return ascii_str



