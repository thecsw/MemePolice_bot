# Fill your Reddit and Telegram API in example.config.py and rename it to config.py
from PIL import Image
import pytesseract
import config
import praw
import cv2
import os, sys
import urllib
import time

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('PewdiepieSubmissions')

banned = ["399","chair","tide","pods","do you know","but can you do this","the way","uganda","noodle","but can","slippy","you do this","skiddadle","skadoodle","upvote if"]

websites = ["youtube","youtu.be","gallery","gif","mp4","webm","gfycat"]

message = """ *Police sounds*

Good day, sir! You have been visited by the **Meme Police!**

I see that you posted an illegal meme on r/PewdiepieSubmissions, *for example: chair memes, tide pods, uganda memes, skiddadle skadoodle, and etc.*

Do not publish old or overused memes here because **only fresh and scrattar memes are allowed!**

You have been warned and please, do not make the same mistake twice. No penalty for now.
______________________

^(Hello there! I am a new AI bot in this subreddit and my duty is to keep order and peace. I do not allow old and overused memes. Meme Police is real.)
"""

def ban(post, text, desc):
    for word in banned:
       if word in text:
           print("Found an illegal meme!")
           post.reply(message)
#           post.downvote()
           print("Will w8 5 mins")
           time.sleep(300)
           return
       if word in desc:
           print("Found an illegal meme!")
           post.reply(message)
#           post.downvote()
           print("Will w8 5 mins")
           time.sleep(300)
           return     

def detect(post):
    if "png" or "jpg" in post.url:
        im = post.id_from_url(post.shortlink)
        desc = post.title
        urllib.urlretrieve(post.url, im)
        print(post)
        print(post.url)
        image = cv2.imread(im)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #gray = cv2.medianBlur(gray, 3)
        filename = "{}-TEST.png".format(im)
        cv2.imwrite(filename, gray)
        img = Image.open(filename)
        text = pytesseract.image_to_string(img).lower()
        os.remove(filename)
        os.remove(im)
        print(text)
        ban(post, text, desc)            

#for submission in subreddit.stream.submissions():
#for submission in subreddit.top('day', limit=25):
for submission in subreddit.hot():
    post = reddit.submission(submission)
    if "gallery" in post.url:
        continue
    if "youtube" in post.url:
        continue
    if "youtu.be" in post.url:
        continue
    if "gif" in post.url:
        continue
    if "mp4" in post.url:
        continue
    if "gfycat" in post.url:
        continue
    if "webm" in post.url:
        continue
    if "v.redd" in post.url:
        continue
    if "facebook" in post.url:
        continue
    if "videos" in post.url:
        continue
    if "imgur" in post.url:
        continue
    if "twitter" in post.url:
        continue
    if "instagram" in post.url:
        continue
    
    if "png" in post.url:
        detect(post)
        continue
    elif "jpg" in post.url:
        detect(post)
        continue
