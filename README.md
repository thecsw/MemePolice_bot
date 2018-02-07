# MemePolice_bot

This is a reddit bot that finds old or not funnny posts and images on r/PewdiepieSubmissions subreddit. When the bot finds an illegal meme, the OP will receive the message below. This bot was created as a joke and later on was improved a little bit. 

<img src="https://i.imgur.com/DFdBGql.png">

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```bash
sudo pip install praw
sudo pip install python-opencv
sudo pip install pytesseract
sudo pip install Pillow
sudo pip install tqdm
```

OR

```
pip install -r requirements.txt
```

[praw](https://github.com/praw-dev/praw) is Python Reddit API Wrapper. This will be the main and only package to connect to Reddit's API and extract desired data.

[python-opencv](https://pypi.python.org/pypi/opencv-python) is used for image transformations and computer vision problems.

[pytesseract](https://pypi.python.org/pypi/pytesseract) is a python wrapper for Google's Tesseract-OCR.

[Pillow](https://pillow.readthedocs.io/en/latest/) is the Python Imaging Library by Fredrik Lundh and Contributors.

[tqdm](https://pypi.python.org/pypi/tqdm) is used for fancy progress bars.

### Other dependencies

Tesseract engine should be installed on a local machine to run the text recognition properly.

#### Debian, Ubuntu (aptitude)
```
sudo apt-get install tesseract-ocr
```

#### Arch Linux (pacman)

```
sudo pacman -S tesseract-ocr
```

I don't know what about other distros. I think tesseract-ocr is included in all package managers.

### Installing

Nothing too complicated. The source code is written in python, so no worries.

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

Config file is ready and you are good to go!

Just run this

```bash
python __main__.py
```

OR

```bash
python src
```
That is everything. The script now just runs and any user that is connected to your Telegram bot can input a number and the bot will retrieve the necessary information.

## Source code

I know that the script is little bit messy, I tried. Simple and small, but it works!

The code is heavily commented and all the important modules are being separated into different files. Look pretty.

## Built With

* [praw](https://github.com/praw-dev/praw) is Python Reddit API Wrapper. This will be the main and only package to connect to Reddit's API and extract \
desired data.
* [python-opencv](https://pypi.python.org/pypi/opencv-python) is used for image transformations and computer vision problems.
* [pytesseract](https://pypi.python.org/pypi/pytesseract) is a python wrapper for Google's Tesseract-OCR.
* [Pillow](https://pillow.readthedocs.io/en/latest/) is the Python Imaging Library by Fredrik Lundh and Contributors.
* [tqdm](https://pypi.python.org/pypi/tqdm) is used for fancy progress bars.

## Authors

* **Sagindyk Urazayev** - *Initial work* - [thecsw](https://github.com/thecsw)
* **Justin Schwaitzberg** - *Rewriting and structuring* - [Schwaitz](https://github.com/Schwaitz)

## Acknowledgments

* Fedora tip to jarhill0 for helping rewriting the code, structuring it and making it fancier. 

## License

This project is licensed under the The GNU General Public License - see the [LICENSE.md](https://github.com/thecsw/MemePolice_bot/blob/master/LICENSE) file for details) explains it pretty well. 
