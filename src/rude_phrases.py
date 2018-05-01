# This is a dictionary of rude phrases in which to reply.
# If a user replies to MemePolice_bot with one of these phrases, the bot will reply to them.
# Note: The word list is an example, as to not have a file of obscenities on the GitHub

import random
import praw

rude_list = [
    "frick you",
    "you suck",
    "go to heck"
]

rude_reply_list = [
    "Well that's pretty rude.",
    """**Police sounds**
    
    You've been charged with being a complete ass.
    """,
    """**Police sounds**
    
        You've been charged cussing on a ***Christian Subreddit***.
    """,
    "Well I'm sorry you feel that way.",
    "I know you are but what am I?",
    "You're literally spending time and effort to insult a bot on the internet.",
    "This is a ***Christian Subreddit***. Please keep your cussing to a minimum.",
    """Careful with the cussing, kids could be watching.
    
    ***Christian Subreddit***
    """,
    "***Christian Subreddit***",
    "Do you kiss your mother with that mouth?"
]


def rudeness_reply(c):
    write_to_rude_log("Replied to " + c.author + "'s comment: " + c.body + "\n\n")
    c.reply(rude_reply_list[random.randint(0, len(rude_reply_list) - 1)])


def alt_rudeness_reply(c, text):
    write_to_rude_log("Replied to " + c.author + "'s comment: " + c.body + " with " + text + "\n\n")
    c.reply(text)


def write_to_rude_log(text):
    file = open("./rudeness/rudeness_log.txt", "a")
    file.write(text)
    file.close()
