# Fill your Reddit and Telegram API in example.config.py and rename it to config.py
from PIL import Image
import argparse
import pytesseract
import config
import praw
import cv2
import os, sys
import urllib

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('PewdiepieSubmissions')

banned = ["399","chair","tide","pods","do you know","but can you do this","but can you"]

message = """ *Beep Boop and police sounds*

Good day, sir! You have been visited by meme police!

I see that you posted an illegal meme in r/PewdiepieSubmissions, for example: chair memes, tide pods, uganda memes and etc.

Do not publish old or overused memes here because only fresh and scrattar memes are allowed!

You have been warned and please, do not make the same mistake twice.

And also, I give you a penalty of 1 downvote.

______________________

Hello there! I am a new AI bot in this subreddit and my duty is to keep order and peace.
I do not allow old and overused memes.
I use advanced and cutting-edge technologies to detect stale memes and will report them to the administration.
If you have any suggestions, reply to my bot and I will read them!
Meme police is real.
"""


for submission in subreddit.hot(limit=10):
    post = reddit.submission(submission)
    if "png" or "jpg" in post.url:
        im = "{}".format(post.id_from_url(post.shortlink))
        desc = submission.title
        urllib.urlretrieve(post.url, im)
        print(post)
        print(post.url)
        print()
        image = cv2.imread(im)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #gray = cv2.medianBlur(gray, 3)
        filename = "test.png"
        cv2.imwrite(filename, gray)
        img = Image.open("test.png")
        text = pytesseract.image_to_string(img).lower()
        os.remove(filename)
        print(text)
        for word in banned:
            if word in text:
                post.reply(message)
                post.downvote
                return
            if word in desc:
                post.reply(message)
                post.downvote
                return
            
