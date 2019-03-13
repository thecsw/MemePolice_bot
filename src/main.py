# Fill your Reddit and Telegram API in example.config.py and rename it to config.py

'''
 __  __                       ____       _ _          
|  \/  | ___ _ __ ___   ___  |  _ \ ___ | (_) ___ ___ 
| |\/| |/ _ \ '_ ` _ \ / _ \ | |_) / _ \| | |/ __/ _ \
| |  | |  __/ | | | | |  __/ |  __/ (_) | | | (_|  __/
|_|  |_|\___|_| |_| |_|\___| |_|   \___/|_|_|\___\___|
       
'''

# This is the message that users receive about illegal memes
from message import message, mention, damages, bl_message
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

# Tesseract-OCR package can work only with jpeg, jpg, png,c gif, bmp files. Reject all other urls
pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")


# Sends a reply to users
def ban(post, place, violation):
    print("Found an illegal word in {}!".format(place))

    title = post.title.encode('utf-8').lower()

    file = open("./logs/violations_log.txt", 'a')
    file.write(str(title) + " at " + time.strftime("%b %d, %Y - %I:%M:%S") + "\n")
    file.close()

    # Save violation
    save_violation(violation)

    # Replace the text %VIOLATION% with the violating word
    message_to_send = message.replace("%VIOLATION%", violation)

    post.reply(message_to_send)


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
                log_to_file("Failed to write to users.json at " + time.strftime("%b %d, %Y - %I:%M:%S"))

        else:
            users_json[user] = 1

            try:
                file = open("./users/users.json", 'w')
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
        file = open("./violations/violations.json", 'r')
        violations_json = json.loads(file.read())
        file.close()

        if v in violations_json.keys():
            violations_json[v] = int(violations_json.get(v)) + 1

            try:
                file = open("./violations/violations.json", 'w')
                file.write(json.dumps(violations_json))
                file.close()
            except:
                log_to_file("Failed to write to violations.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))

        else:
            violations_json[v] = 1

            try:
                file = open("./violations/violations.json", 'w')
                file.write(json.dumps(violations_json))
                file.close()
            except:
                log_to_file("Failed to write to violations.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))
    except:
        log_to_file("Failed to read violations.json at" + time.strftime("%b %d, %Y - %I:%M:%S"))
        file = open("./violations/violations.json", 'w')
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

                    meme_text = ""

                    try:
                        meme_text = str(text_recognition(post).lower())
                    except Exception as e:
                        print(e)
                    print("\tImage Text: {}".format(meme_text))

                    if "bitch lasagna" in meme_text or "bitch lasagna" in str(title):
                        message_to_send = bl_message
                        post.reply(message_to_send)
                        continue

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
                    if "bitch lasagna" in str(title):
                        message_to_send = bl_message
                        post.reply(message_to_send)
                        continue

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

            check = open("./checked_comments.txt", 'r')
            checked = check.readlines()
            check.close()

            if c.id + "\n" not in checked:
                file = open("./checked_comments.txt", "a")
                file.write(c.id + "\n")
                file.close()

                if "memepolice" not in str(c.author.name.encode("utf-8").lower()):  # We don't need to parse our own comments
                    summon_bot(c)
                    parse_comment(c)
                    reply_to_comments(c)
        time.sleep(30)


def reply_to_comments(c):
    try:
        text = str(c.body.encode("utf-8").lower())  # c.body is a byte-like object but we need str

        if "ur mom gay" in text or "your mom gay" in text:
            alt_rudeness_reply(c, "no u")
            return

        elif "good bot" in text:
            alt_rudeness_reply(c, "Good human :)")
            return

        elif "bad bot" in text:
            alt_rudeness_reply(c, "My creators specifically programmed me to feel physical pain when people say I'm bad. I hope you're happy :(")
            return

        elif "no u" in text:
            alt_rudeness_reply(c, damages[random.randint(0, len(damages) - 1)])
            return

        for w in rude_list:
            if w in text:
                rudeness_reply(c)
                break

    except Exception as e:
        print("Something bad happened in reply_to_comments: {}".format(e))


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
            if comment.ups < -2:
                comment.delete()

        # 1 hour of sleep
        time.sleep(3600)


def threads():
    Thread(name="Submissions", target=submission_thread).start()
    Thread(name="Comments", target=comment_thread).start()
    Thread(name="Save Karma", target=save_karma).start()


def main():
    threads()
