def log_to_file(text):
    file = open("./log/log.txt", "a")
    file.write(text + "\n")
    file.close()