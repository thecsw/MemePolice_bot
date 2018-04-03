import praw
import json
import time
import re

from utils import log_to_file

words = []
replace_chars = ['"', '.', ';', ':', '?', '!', '*', '+', '-', '(', ')', '[', ']', '{', '}', '>', '<', ',', '^', '@',
                 '$', '%', '&', '_', '=', '\n', '|', '\\', "#", '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

word = ""

words_json = {}

file_length = -1


def init_analyzation():
    try:
        global words_json

        file = open("./data-analyzation/words.json", 'r')
        words_json = json.loads(file.read())
        file.close()

        file_length = len(words_json)
    except Exception as e:
        print("Failed during init_analyzation: {}".format(e))

def parse_comment(c):

    check = open("./data-analyzation/checked.txt", 'r')
    checked = check.readlines()
    check.close()

    if c.id + "\n" not in checked:
        print("Reading comment " + c.id + " at " + time.strftime("%b %d, %Y - %I:%M:%S") + " by " + str(c.author))

        file = open("./data-analyzation/checked.txt", "a")
        file.write(c.id + "\n")
        file.close()

        for w in c.body.split(' '):
            if "http" in w or "/u/" in w or "/r/" in w or "\\" in str(w.encode('utf-8')):
                continue

            word = w
            for ch in replace_chars:
                word = word.replace(ch, '')

            if word != "" and word != " " and word != "'" and word != "," and word != '\n' and word[0] != "'" and "\\u" not in repr(word):
                try:
                    file = open("./data-analyzation/words.json", 'r')
                    words_json = json.loads(file.read())
                    file.close()
                except:
                    log_to_file("Failed to read words.json at " + time.strftime("%b %d, %Y - %I:%M:%S"))
                    continue

                if word in words_json.keys():
                    words_json[word] = int(words_json.get(word)) + 1
                else:
                    words_json[word] = 1

                new_file_length = len(words_json)

                if new_file_length > file_length - 100:
                    try:
                        file = open("./data-analyzation/words.json", 'w')
                        file.write(json.dumps(words_json))
                    except:
                        log_to_file("Failed to write words.json at " + time.strftime("%b %d, %Y - %I:%M:%S"))
                else:
                    log_to_file("Length discrepancy in words.json at " + time.strftime(" % b % d, % Y - % I: % M: % S"))

                file.close()
