import praw
import json
import time
import re


# The config file with reddit API credentials
import config as config

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewdiepiesubmissions')


words = []
replace_chars = ['"', '.', ';', ':', '?', '!', '*', '+', '-', '(', ')', '[', ']', '{', '}', '>', '<', ',', '^', '@',
                 '$', '%', '&', '_', '=', '\n', '|', '\\', "#", '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



word = ""

file = open("./words.json", 'r')
words_json = json.loads(file.read())
file.close()

file_length = len(words_json)

print("\nProgram Started at " + time.strftime("%b %d, %Y - %I:%M:%S") + "\n")

for c in subreddit.stream.comments():
    try:
        print("Reading comment " + c.id + " at " + time.strftime("%b %d, %Y - %I:%M:%S"))
        check = open("./checked.txt", 'r')
        checked = check.readlines()
        check.close()

        if c.id + "\n" not in checked:
            file = open("./checked.txt", "a")
            file.write(c.id + "\n")
            file.close()


            for w in c.body.split(' '):
                if "http" in w or "/u/" in w or "/r/" in w or "\\" in w:
                    continue

                word = w
                for ch in replace_chars:
                    word = word.replace(ch, '')

                if word != "" and word != " " and word != "'" and word != "," and word != '\n' and word[0] != "'" and "\\u" not in repr(word):
                    try:
                        file = open("./words.json", 'r')
                        words_json = json.loads(file.read())
                        file.close()
                    except:
                        print("Error reading file at " + time.strftime("%b %d, %Y - %I:%M:%S"))
                        continue

                    if word in words_json.keys():
                        words_json[word] = int(words_json.get(word)) + 1
                    else:
                        words_json[word] = 1

                    new_file_length = len(words_json)

                    if new_file_length > file_length - 100:
                        try:
                            file = open("./words.json", 'w')
                            file.write(json.dumps(words_json))
                        except:
                            print("Error writing file at " + time.strftime("%b %d, %Y - %I:%M:%S"))
                    else:
                        print("Length discrepancy at" + time.strftime(" % b % d, % Y - % I: % M: % S"))

                    file.close()
    except:
        print("Error reading stream at " + time.strftime("%b %d, %Y - %I:%M:%S"))
