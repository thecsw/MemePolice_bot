# Fill your Reddit and Telegram API in example.config.py and rename it to config.py

# This is the message that users receive about illegal memes
from message import message, mention
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

# JSON Parsing
import json

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewdiepiesubmissions')
# subreddit = reddit.subreddit('test')

# Tesseract-ocr package can work only with jpeg, jpg, png, gif, bmp files. Reject all other urls
pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")


# Sends a reply to users
def ban(post, place):
    print("Found an illegal word in {}!".format(place))
    post.reply(message)
    time.sleep(60)


def save_user(user):
    try:
        file = open("./users/users.json", 'r')
        users_json = json.loads(file.read())
        file.close()

        if user in users_json.keys():
            users_json[user] = int(users_json.get(user)) + 1

            try:
                file = open("./users/users.json", 'w')
                file.write(json.dumps(users_json))
                file.close()
            except:
                print("Failed to write to users.json")

        else:
            users_json[user] = 1

            try:
                file = open("./users/users.json", 'w')
                file.write(json.dumps(users_json))
                file.close()
            except:
                print("Failed to write to users.json")
    except:
        print("Failed to read users.json")
        file = open("./users/users.json", 'w')
        file.write("{}")
        file.close()


def submission_thread():
    while True:
        for submission in tqdm(subreddit.stream.submissions()):

            post = reddit.submission(submission)
            # Sometimes the submissions' titles include non-ASCII symbols. Need to validate and encode.
            # All the banned words are in lowercase, that is why we need to convert it to lowercase.
            title = post.title.encode('utf-8').lower()

            checked = open("./checked.txt", 'r')
            check = checked.readlines()
            checked.close()

            if post.id + "\n" not in check:
                print("Reading Submission '" + str(title) + "' at " + time.strftime("%b %d, %Y - %I:%M:%S") + " by " + str(post.author))

                checked = open("./checked.txt", "a")
                checked.write(post.id + "\n")
                checked.close()

                if pattern.search(post.url) is not None:
                    print("\tMatched regex, post is an image")
                    try:
                        meme_text = text_recognition(post).lower()
                    except:
                        continue
                    print("\tImage Text: {}".format(meme_text))
                    for word in illegal_memes:
                        if word in meme_text:

                            # Save user data
                            save_user(str(post.author))

                            # Comment on post
                            ban(post, "image")
                            break
                        # If not found in recognized text, analyze title
                        elif word in str(title):

                            # Save user data
                            save_user(str(post.author))

                            # Comment on post
                            ban(post, "image")
                            break

                else:
                    for word in illegal_memes:
                        if word in str(title):

                            # Save user data
                            save_user(str(post.author))

                            # Comment on post
                            ban(post, "image")
                            break
            else:
                print("Already checked meme, skipping")
        time.sleep(60)


def comment_thread():
    while True:
        for c in subreddit.stream.comments():
            try:
                if "u/memepolice_bot" in c.encode("utf-8").lower: # Somebody mentioned us, maybe to come?
                    c.submission.reply(message)
                    c.reply(mention)
                parse_comment(c)
            except:
                print("Error reading stream at " + time.strftime("%b %d, %Y - %I:%M:%S"))

        time.sleep(60)

def save_karma():
    memepolice = reddit.redditor("MemePolice_bot")
    while True:
        for comment in memepolice.comments.new(limit=100):
            # It will parse 100 comments in 5-6 seconds
            # print(comment.fullname)
            # print(comment.ups)
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
