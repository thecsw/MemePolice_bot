# Collatz Bot

Telegram bot that takes some natural number as an input and calculates a particular case of Collatz Conjecture with that number. Makes a graph of every step and also analyzes data to output at the end of the process.

What is Collatz Conjecture? [Wikipedia](https://en.wikipedia.org/wiki/Collatz_conjecture) explains it pretty well. 


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

[telepot](https://github.com/nickoala/telepot) is a python framework for Telegram Bot API. This package will be used to connect to Telegram API and to communicate with users over the internet.

[matplotlib](https://matplotlib.org/) is a Python plotting library that does its job very and very well. 

About numpy and scipy, it is little bit redundant to manually install numpy and scipy as everything essential is already included in the matplotlib's dependencies. However, I just do it to be sure. 

### Installing

Nothing too complicated. The source code is written in python, so no worries.

The only thing that needs to be done before execution is the config profile. In the config profile you should fill your Telegram Bot's unique API key.

For that please follow these steps

```bash
git clone https://github.com/thecsw/collatz
cd collatz
mv example.config.py config.py
nano config.py
```

Now here, you can use any text editor you like. When opening the file you will see this

```python
token = 'YOUR TELEGRAM API KEY'
```

So what will you need to do now is to get your Telegram API token from [BotFather](https://telegram.me/botfather)

After filling out the key, save and exit. You're done with installation.

## Deployment

Config file is ready and you are good to go!

Just run this

```bash
python collatz.py
```

That is everything. The script now just runs and any user that is connected to your Telegram bot can input a number and the bot will retrieve the necessary information.

## Source code

I know that the script is little bit messy, I tried. Simple and small, but it works!

Now, I want to give little insight on the code. 

```python
plt.savefig('Graph{}.png'.format(num), dpi=500, format='png')
plt.savefig('Graph{}.svg'.format(num), dpi=500, format='svg')
```
These lines handle the image processing and graph saving. dpi obviously means resolution/quality in DPI (Dots per Inch). I found that 500 is quite optimal, so I just use it. If you want bigger resolution, just change values in these and that's all. Maybe I should make a separate variable.

Also, all saved graphs are always automatically deleted. If they were not created, there will still be an attempt to delete them.

## Built With

* [telepot](https://github.com/nickoala/telepot) - python framework for Telegram Bot API.
* [matplotlib](https://github.com/praw-dev/praw) - Python plotting library.

## Authors

* **Sagindyk Urazayev** - *Initial work* - [thecsw](https://github.com/thecsw)
* **jarhill0** - *Rewriting and structuring* - [jarhill0](https://github.com/jarhill0)

## Acknowledgments

* Fedora tip to jarhill0 for helping rewriting the code, structuring it and making it fancier. 

## License

This project is licensed under the The GNU General Public License - see the [LICENSE.md](https://github.com/thecsw/rjokes/blob/master/LICENSE) file for details) explains it pretty well. 
