# Fill your Reddit and Telegram API in example.config.py and rename it to config.py

# This is the message that users receive about illegal memes
from message import message
# This file contains one method to input an image and output found text
from text_recognition import text_recognition
# Dictionary of banned words
from blacklist import illegal_memes
# The config file with reddit API credentials
import config as config
# For the cooldown purposes, see below
import time

# Tracking iterations
from tqdm import tqdm
# Python Reddit API Wrapper. Self-explanatory
import praw

# Finding a pattern
import re

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewdiepiesubmissions')

# Tesseract-ocr package can work only with jpeg, jpg, png, gif, bmp files. Reject all other urls
pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")

# Sends a reply to users
def ban(post,place):
    print("Found an illegal word in{}!".format(place))
    post.reply(message)
    # Reddit API has a limitations of actions performed per short period of time.
    # So a cooldown of 1 minute is proven to be enough
    time.sleep(60)


if __name__ == "__main__":
    while True:
        for submission in tqdm(subreddit.stream.submissions()):
            post = reddit.submission(submission)
            # Sometimes the submissions' titles include non-ASCII symbols. Need to validate and encode.
            # All the banned words are in lowercase, that is why we need to convert it to lowercase.
            title = post.title.encode('utf-8').lower()
            print("Title: {}".format(title))
            
            if pattern.search(post.url) is not None:
                print("\tMatched regex, post is an image")
                try:
                    meme_text = text_recognition(post).lower()
                except:
                    continue
                print("\tImage Text: {}".format(meme_text))
                for word in illegal_memes:
                    if word in meme_text:
                        ban(post,"image")
                    # If not found in recognized text, analyze title
                    elif word in title:
                        ban(post,"title")

            else:
                for word in illegal_memes:
                    if word in title:
                        ban(post,"title")
else:
    pass
