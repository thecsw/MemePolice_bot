# Fill your Reddit and Telegram API in example.config.py and rename it to config.py
from message import message
from text_recognition import text_recognition
from blacklist import illegal_memes
from tqdm import tqdm
import config
import praw
import time

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('PewdiepieSubmissions')

def ban(post, recognized_text, desc):
    for word in illegal_memes:
       if word in recognized_text:
           print("Found an illegal meme!")
           post.reply(message)
           print("Will w8 1 min")
           time.sleep(60)
           return
       if word in desc:
           print("Found an illegal meme!")
           post.reply(message)
           print("Will w8 1 min")
           time.sleep(60)
           return     

if __name__ == "__main__":
    while 1:        
        for submission in tqdm(subreddit.stream.submissions()):
            print("\nStarting new meme!")
            post = reddit.submission(submission)
            title = post.title.encode('utf-8').lower()
            print("Submission title -> {}".format(title))
            if "png" in post.url:
                meme_text = text_recognition(post)
                print("Meme text -> \n {}".format(meme_text))
                ban(post, meme_text, title)
                continue
            elif "jpg" in post.url:
                meme_text = text_recognition(post)
                print("Meme text -> \n {}".format(meme_text))
                ban(post, meme_text, title)
                continue
