# Fill your Reddit and Telegram API in example.config.py and rename it to config.py

'''
 __  __                       ____       _ _          
|  \/  | ___ _ __ ___   ___  |  _ \ ___ | (_) ___ ___ 
| |\/| |/ _ \ '_ ` _ \ / _ \ | |_) / _ \| | |/ __/ _ \
| |  | |  __/ | | | | |  __/ |  __/ (_) | | | (_|  __/
|_|  |_|\___|_| |_| |_|\___| |_|   \___/|_|_|\___\___|
       
'''

# This is the message that users receive about illegal memes
from message import message, mention, damages
# This file contains one method to input an image and output found text
from text_recognition import text_recognition
# Dictionary of banned words
from blacklist import illegal_memes
# The config file with reddit API credentials
import config as config

# The rude phrases reply list and function
from rude_phrases import rude_list, rude_reply_list, rudeness_reply, alt_rudeness_reply

# For the cooldown purposes, see below
import time

# For analyzing and saving comment words
from analyze import parse_comment

# Assorted Utilities
from utils import log_to_file

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

import random

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewdiepiesubmissions')

violations_file = "./violations/violations.json"
violations_log_file = "./logs/violations_log.txt"
users_file = "./users/users.json"
checked_file = "./checked.txt"
rude_checked_file = "./rudeness/checked.txt"
rude_log_file = "./rudeness/rudeness_log.txt"

# Tesseract-OCR package can work only with jpeg, jpg, png, gif, bmp files. Reject all other urls
pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")


# Sends a reply to users
def ban(post, place, violation):
    print("Found an illegal word in {}!".format(place))

    title = post.title.encode('utf-8').lower()

    file = open(violations_log_file, 'a')
    file.write(str(title) + " at " + time.strftime("%b %d, %Y - %I:%M:%S") + "\n")
    file.close()

    # Save violation
    save_violation(violation)

    # Replace the text %VIOLATION% with the violating word
    message_to_send = message.replace("%VIOLATION%", violation)

    post.reply(message_to_send)


def save_user(user):
    try:
        file = open(users_file, 'r')
        users_json = json.loads(file.read())
        file.close()

        if user in users_json.keys():
            users_json[user] = int(users_json.get(user)) + 1

            try:
                file = open(users_file, 'w')
                file.write(json.dumps(users_json))
                file.close()
            except:
                log_to_file("Failed to write to users.json at " + time.strftime("%b %d, %Y - %I:%M:%S"))

        else:
            users_json[user] = 1

            try:
                file = open(users_file, 'w')
                file.write(json.dumps(users_json))
                file.close()
            except:
                log_to_file("Failed to write to users.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))
    except:
        log_to_file("Failed to read users.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))
        file = open("./users/users.json", 'w')
        file.write("{}")
        file.close()


def save_violation(v):
    try:
        file = open(violations_file, 'r')
        violations_json = json.loads(file.read())
        file.close()

        if v in violations_json.keys():
            violations_json[v] = int(violations_json.get(v)) + 1

            try:
                file = open(violations_file, 'w')
                file.write(json.dumps(violations_json))
                file.close()
            except:
                log_to_file("Failed to write to violations.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))

        else:
            violations_json[v] = 1

            try:
                file = open(violations_file, 'w')
                file.write(json.dumps(violations_json))
                file.close()
            except:
                log_to_file("Failed to write to violations.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))
    except:
        log_to_file("Failed to read violations.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))
        file = open(violations_file, 'w')
        file.write("{}")
        file.close()


def submission_thread():
    while True:
        for submission in tqdm(subreddit.stream.submissions()):

            post = reddit.submission(submission)
            # Sometimes the submissions' titles include non-ASCII symbols. Need to validate and encode.
            # All the banned words are in lowercase, that is why we need to convert it to lowercase.
            title = post.title.encode('utf-8').lower()

            checked = open(checked_file, 'r')
            check = checked.readlines()
            checked.close()

            if post.id + "\n" not in check:
                print("Reading Submission '" + str(title) + "' at " + time.strftime("%b %d, %Y - %I:%M:%S") + " by " + str(post.author))

                checked = open(checked_file, "a")
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
                            ban(post, "image", word)
                            break

                        # If not found in recognized text, analyze title
                        elif word in str(title):
                            # Save user data
                            save_user(str(post.author))

                            # Comment on post
                            ban(post, "image", word)
                            break

                else:
                    for word in illegal_memes:
                        if word in str(title):
                            # Save user data
                            save_user(str(post.author))

                            # Comment on post
                            ban(post, "image", word)
                            break
            else:
                print("Already checked post, '" + str(title) + "' - skipping")
        time.sleep(60)


def comment_thread():
    while True:
        for c in subreddit.stream.comments():
            if "memepolice" not in str(c.author.name.encode("utf-8").lower()):  # We don't need to parse our own comments
                summon_bot(c)
                parse_comment(c)
        time.sleep(30)


def summon_bot(c):
    try:
        text = str(c.body.encode("utf-8").lower())  # c.body is a byte-like object but we need str
        if "u/memepolice" in text:
            c.reply(mention)
            ban(c.submission, "image", "I was called!")
            print("summon_bot triggered!")
    except Exception as e:
        print("Something bad happened in summon_bot: {}".format(e))


def save_karma():
    memepolice = reddit.redditor("MemePolice_bot")
    while True:
        for comment in memepolice.comments.new(limit=100):
            # It will parse 100 comments in 5-6 seconds
            if comment.ups < -1:
                comment.delete()

        # 1 hour of sleep
        time.sleep(3600)


def rude_reply_thread():
    while True:
        for m in reddit.inbox.comment_replies():
            check = open(rude_checked_file, 'r')
            checked = check.readlines()
            check.close()

            if m.id + "\n" not in checked:
                file = open(rude_checked_file, "a")
                file.write(m.id + "\n")
                file.close()

                body = str(m.body.encode("utf-8").lower())

                if "ur mom gay" in body or "your mom gay" in body:
                    alt_rudeness_reply(m, "no u")
                    continue

                if "no u" in body:
                    alt_rudeness_reply(m, damages[random.randint(0, len(damages) - 1)])
                    continue

                for w in rude_list:
                    if w in m.body:
                        rudeness_reply(m)
                        break

        # 15 minutes of sleep
        time.sleep(900)


def threads():
    Thread(name="Submissions", target=submission_thread).start()
    Thread(name="Comments", target=comment_thread).start()
    Thread(name="Save Karma", target=save_karma).start()
    Thread(name="Rudeness", target=rude_reply_thread).start()


def main():
    threads()
