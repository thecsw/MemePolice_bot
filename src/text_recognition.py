import urllib
import os, sys
import pytesseract
import cv2
from PIL import Image


def text_recognition(post):
    meme_name = "temp"
    # Download the image
    urllib.urlretrieve(post.url, filename=meme_name)
    image = cv2.imread(meme_name)
    # Next 3 lines are needed to prepare an image for text recognition
    # However, line 17 can be commented out as it is not very important and has been added just in case of noisy images
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    filename = "{}-ocr.png".format(meme_name)
    cv2.imwrite(filename, gray)
    img = Image.open(filename)
    # We need to encode it as utf-8
    recognized_text = pytesseract.image_to_string(img).encode('utf-8')
    # Little cleanup
    os.remove(filename)
    os.remove(meme_name)
    return recognized_text
