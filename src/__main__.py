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

# For analyzing and saving comment words
from analyze import init_analyzation
from analyze import parse_comment

# Tracking iterations
from tqdm import tqdm
# Python Reddit API Wrapper. Self-explanatory
import praw

# Finding a pattern
import re

# Multi-threading
from threading import Thread

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewdiepiesubmissions')

# Tesseract-ocr package can work only with jpeg, jpg, png, gif, bmp files. Reject all other urls
pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")


# Sends a reply to users
def ban(post, place):
    checked = open("./checked.txt", 'r')
    check = checked.readlines()
    checked.close()

    if post.id not in check:
        print("Found an illegal word in{}!".format(place))
        checked = open("./checked.txt", "a")
        checked.write(post.id + "\n")
        checked.close()

        post.reply(message)
        time.sleep(60)


def submission_thread():
    while True:
        for submission in tqdm(subreddit.stream.submissions()):





            post = reddit.submission(submission)
            # Sometimes the submissions' titles include non-ASCII symbols. Need to validate and encode.
            # All the banned words are in lowercase, that is why we need to convert it to lowercase.
            title = post.title.encode('utf-8').lower()
            print("Reading Submission '" + str(title) + "' at " + time.strftime("%b %d, %Y - %I:%M:%S"))

            if pattern.search(post.url) is not None:
                print("\tMatched regex, post is an image")
                try:
                    meme_text = text_recognition(post).lower()
                except:
                    continue
                print("\tImage Text: {}".format(meme_text))
                for word in illegal_memes:
                    if word in meme_text:
                        ban(post, "image")
                        break
                    # If not found in recognized text, analyze title
                    elif word in str(title):
                        ban(post, "title")

                        break

            else:
                for word in illegal_memes:
                    if word in str(title):
                        ban(post, "title")
                        break


def comment_thread():
    while True:
        for c in subreddit.stream.comments():
            try:
                parse_comment(c)
            except:
                print("Error reading stream at " + time.strftime("%b %d, %Y - %I:%M:%S"))

def save_karma():
    memepolice = reddit.redditor("MemePolice_bot")
    while True:
        for comment in memepolice.comments.new(limit=100):
            # It will parse 100 comments in 5-6 seconds
            #print(comment.fullname)
            #print(comment.ups)
            if (comment.ups < -1):
                comment.delete()
    # We will wait an hour for downvotes to come
    time.sleep(3600)
                
if __name__ == "__main__":
    init_analyzation()
    
    Thread(name="Save Karma", target=save_karma).start()
    Thread(name="Submissions", target=submission_thread).start()
    Thread(name="Comments", target=comment_thread).start()
else:
    pass
