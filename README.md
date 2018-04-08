# MemePolice_bot

This is a reddit bot that finds old or not funnny posts and images on r/PewdiepieSubmissions subreddit. When the bot finds an illegal meme, the OP will receive the message below. This bot was created as a serious project (joke-ish) and later on was improved a little bit. 

<img src="https://i.imgur.com/DFdBGql.png">

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```bash
sudo pip install praw
sudo pip install python-opencv
sudo pip install pytesseract
sudo pip install tesseract-ocr
sudo pip install Pillow
sudo pip install tqdm
```

OR

```
pip install --upgrade -r requirements.txt
```

[praw](https://github.com/praw-dev/praw) is Python Reddit API Wrapper. This will be the main and only package to connect to Reddit's API and extract desired data.

[python-opencv](https://pypi.python.org/pypi/opencv-python) is used for image transformations and computer vision problems.

[pytesseract](https://pypi.python.org/pypi/pytesseract) is a python wrapper for Google's Tesseract-OCR.

[Pillow](https://pillow.readthedocs.io/en/latest/) is the Python Imaging Library by Fredrik Lundh and Contributors.

[tqdm](https://pypi.python.org/pypi/tqdm) is used for fancy progress bars.

### Other dependencies

Tesseract engine should be installed on a local machine to run the text recognition properly. We will also install the tesseract OCR trained languages for better accuracy and we will install only the English packages. For more information about other languages, please refer to tesseract's official [repository on Github](https://github.com/tesseract-ocr/tesseract).

#### Linux

##### Debian, Ubuntu (aptitude)
```
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng
```

##### Arch Linux (pacman)

```
sudo pacman -S tesseract
sudo pacman -S tesseract-data-eng
```

#### Mac OS

##### Homebrew

```
brew install tesseract
```

I don't know what about other distros. I think tesseract-ocr is included in all package managers.

If you want to compile the tesseract engine  by yourself, please refer to the [official guides.](https://github.com/tesseract-ocr/tesseract/wiki/Compiling).

### Installing

The only thing that needs to be done before execution is the config profile. In the config profile you should fill your Reddit API details.

For that please follow these steps

```bash
git clone https://github.com/thecsw/MemePolice_bot
cd MemePolice_bot
mv example.config.py config.py
nano config.py
```

After filling out the details, save and exit. You're done with installation.

## Deployment

Remove the word **'example'** from the title of all files with it.

Just run this

```bash
python __main__.py
```

That is everything. All illegal memes shall be found and OPs should be punsihed.

## Source code

The code is heavily commented and all the important modules are being separated into different files. Looks pretty, dunno.

Here is a short description of all the source files

- `analyze.py` - Heavy file on analyzing comments and filling them in needed files.
- `blacklist.py` - Contains all the banned keywords that will trigger the bot to respond.
- `config.example.py` - Just the PRAW (OAuth) credentials for bot initialization.
- `main.py` - The main script that processses everything and has the main loop with threads.
- `message.py` - Different messages that bot will send to users.
- `rude_phrases.py` - Bot's responses to rude replies.
- `text_recognition.py` - Returns text read from an image.
- `utils.py` - Just the logging and other technical stuff.
- `__main__.py` - The file that should be executed.

Here is a short description of .json and .txt files that we have

- `./users/users.json` - this is a list of offenders with the number of illegal content posted
- `./data-analyzation/checked.txt` - stores checked comments.
- `./data-analyzation/words.json` - sotres words and their respective frequency.
- `./rudeness/checked.txt` - stores old rude replies.
- `./rudeness/rudeness_log.txt` - stores the logs and other "rude" data.
- `./violations/violations.json` - stores all the violations.
- `./logs/log.txt` - stores errors and other debug information.
- `./logs/violations_log.txt` - debug data for violations.

## Built With

- [praw](https://github.com/praw-dev/praw) is Python Reddit API Wrapper. This will be the main and only package to connect to Reddit's API and extract \
desired data.
- [python-opencv](https://pypi.python.org/pypi/opencv-python) is used for image transformations and computer vision problems.
- [pytesseract](https://pypi.python.org/pypi/pytesseract) is a python wrapper for Google's Tesseract-OCR.
- [Pillow](https://pillow.readthedocs.io/en/latest/) is the Python Imaging Library by Fredrik Lundh and Contributors.
- [tqdm](https://pypi.python.org/pypi/tqdm) is used for fancy progress bars.

## Authors

- **Sagindyk Urazayev** - *Initial work* - [thecsw](https://github.com/thecsw)
- **Justin Schwaitzberg** - *Rewriting, structuring, and adding new features* - [Schwaitz](https://github.com/Schwaitz)

## Acknowledgments

 - Fedora tip to Justin Schwaitzberg for greatly contributing to the code, structuring it and making it fancier. 

## License

This project is licensed under the The GNU General Public License - see the [LICENSE.md](https://github.com/thecsw/MemePolice_bot/blob/master/LICENSE) file for details) explains it pretty well. 
