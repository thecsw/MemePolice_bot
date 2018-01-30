# rjokes

This is a reddit bot, specifically designed for and only 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
sudo pip install pytesseract
sudo pip install praw
```
[telepot](https://github.com/nickoala/telepot) is a python framework for Telegram Bot API. This package will be used to connect to Telegram API and to communicate with users over the internet.

[praw](https://github.com/praw-dev/praw) is Python Reddit API Wrapper. This will be the main and only package to connect to Reddit's API and extract desired data.

### Installing

Nothing too complicated. The source code is written in python, so no worries.

The only thing that needs to be done before execution is the config profile. In the config profile you should fill your Reddit API details and Telegram Bot's unique API key.

For that please follow these steps

```
git clone https://github.com/thecsw/rjokes
cd rjokes
mv example.config.py config.py
nano config.py
```

Now here, you can use any text editor you like. When opening the file you will see this

```python
#This is for reddit
client_id = 'take it from your account\'s preferences'
client_secret = 'take it from your account\'s preferences'
username = 'username'
password = 'password'
user_agent = 'something'
#This is for telegram
token = 'YOUR TELEGRAM API KEY'
```

So what will you need to do now is to get your Reddit API details from [here](https://reddit.com) and your Telegram API token from [BotFather](https://telegram.me/botfather)

After filling out the keys, save and exit.

## Deployment

Config file is ready and you are good to go!

Just run this

```bash
python rjokes.py
```

That is everything. The script now just runs and any user that is connected to your Telegram bot can request a joke via the /joke command.

## Source code

I know that the script is little bit messy, I tried. Simple and small, but it works!

Now, I want to give little insight on the code. If you want to take posts from any other subreddit, in the main source file rjokes.py, change this variable's value to any subrreddit you like

```python
sub = 'Jokes' # Means it will extract posts from reddit.com/r/Jokes
```

Also, this script takes only the best jokes of the last 24 hours and updates them every hour. If you want to change the source of jokes, change this line

```python
hot_python = subreddit.top('day', limit=LIMIT)
```

LIMIT is the amount of posts to extract

Well and also the time interval is in seconds

```python
time.sleep(3600)
```

## Built With

* [telepot](https://github.com/nickoala/telepot) - python framework for Telegram Bot API.
* [praw](https://github.com/praw-dev/praw) - Python Reddit API Wrapper.

## Authors

* **Sagindyk Urazayev** - *Initial work* - [thecsw](https://github.com/thecsw)

## License

This project is licensed under the The GNU General Public License - see the [LICENSE.md](https://github.com/thecsw/rjokes/blob/master/LICENSE) file for details
