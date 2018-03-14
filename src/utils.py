def log_to_file(text):
    file = open("./logs/log.txt", "a")
    file.write(text + "\n")
    file.close()
