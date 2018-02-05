# Fill your Reddit and Telegram API in example.config.py and rename it to config.py
from message import message
from text_recognition import text_recognition
from blacklist import illegal_memes
import config as config
import time

from tqdm import tqdm
import praw

import re

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewdiepiesubmissions')

pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")


def ban(post):
    print("Found an illegal title!")
    post.reply(message)
    time.sleep("60")


if __name__ == "__main__":
    while True:
        for submission in subreddit.stream.submissions():
            post = reddit.submission(submission)
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
                        ban(post)
                    elif word in title:
                        ban(post)

            else:
                for word in illegal_memes:
                    if word in title:
                        ban(post)
else:
    pass
