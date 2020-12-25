# Improved version of subito-it-searcher

BeautifulSoup scraper running queries on a popular italian ad website.
This searcher is compatible with Python 3.x versions.

The original version is from [MorroLinux](https://www.youtube.com/watch?v=qyZ-E-6TPD8)

## The fork
This fork adds:
* Infinite refresh with adjustable delay
* Multiplatform support: can run also on Windows
* Windows 10 notifications
* Easier Telegram setup
* Handle connection errors
* Fix flooding on Telegram

## Configuration
Before using this searcher, you must first install the following external modules through CLI (Windows/Linux/Mac: `pip3 install [modulename]`):
* `requests` (HTTP requests)
* `bs4` (BeautifulSoup)

### Telegram configuration
To have to bot send you updates on Telegram, follow these steps:
1) Create a bot by writing to the BotFather on Telegram
2) BotFather will give you an API key: **save this API key for later**
3) Create a public channel and add the newly created bot as administrator
4) **Save the name of the channel** including the "@", for example: @subito_bot

To configure Telegram, simply invoke the script with the proper parameters as following:

`pyhton3 subito-searcher.py --addtoken [YOUR_API_TOKEN] --addchatid [YOUR_CHANNEL_NAME]`

## Usage
Write `python3 subito-searcher.py --help` to see all the command line arguments. Keep in mind that the script *always* needs some argument in order to start. 

Here is a cheatsheet of the most common usages:

* Add a new query with name "Auto":
`python3 subito-searcher.py --add Auto --url https://www.subito.it/annunci-italia/vendita/usato/?q=auto`
(keep in mind that you *always* use `--add` and `--url` together)

* Remove the query "Auto":
`python3 subito-searcher.py --delete Auto`

* See a list of all your added queries:
`python3 subito-searcher.py --short_list`

* **Start the bot**, it will search for new announcements every 2 minutes:
`python3 subito-searcher.py --daemon`

* Start the bot with a custom delay (example, 30 seconds):
`python3 subito-searcher.py --daemon --delay 30`

* Start the bot, but disable windows notifications:
`python3 subito-searcher.py --notifyoff`

* Start the bot, but disable telegram messages:
`python3 subito-searcher.py --tgoff`
