import praw
import json
import time
import re

from utils import log_to_file

replace_chars = ['"', '.', ';', ':', '?', '!', '*', '+', '-', '(', ')', '[', ']', '{', '}', '>', '<', ',', '^', '@',
                 '$', '%', '&', '_', '=', '\n', '|', '\\', "#", '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

data_words_file = "./data-analyzation/words.json"
data_checked_file = "./data-analyzation/checked.txt"


def parse_comment(c):
    check = open(data_checked_file, 'r')
    checked = check.readlines()
    check.close()

    try:
        file = open(data_words_file, 'r')
        words_json = json.loads(file.read())
        file.close()
        file_length = len(words_json)
    except:
        log_to_file("Failed to read words.json at " + time.strftime("%b %d, %Y - %I:%M:%S"))
        return

    if c.id + "\n" not in checked:
        print("Reading comment " + c.id + " at " + time.strftime("%b %d, %Y - %I:%M:%S") + " by " + str(c.author))

        file = open(data_checked_file, "a")
        file.write(c.id + "\n")
        file.close()

        body = str(c.body.encode('utf-8'))

        for w in body.split(' '):
            word = str(w.encode('utf-8'))

            if "http" in word or "/u/" in word or "/r/" in word or "\\" in word:
                continue

            for ch in replace_chars:
                word = word.replace(ch, '')

            if word is not "" and word is not " " and word is not "'" and word is not "," and word is not '\n' and word[0] is not "'":

                if word in words_json.keys():
                    words_json[word] = int(words_json.get(word)) + 1
                else:
                    words_json[word] = 1

                new_file_length = len(words_json)

                if new_file_length > file_length - 500:
                    try:
                        file = open(data_words_file, 'w')
                        file.write(json.dumps(words_json))
                    except:
                        log_to_file("Failed to write words.json at " + time.strftime("%b %d, %Y - %I:%M:%S"))
                else:
                    log_to_file("Length discrepancy in words.json at " + time.strftime(" % b % d, % Y - % I: % M: % S"))

                file.close()
