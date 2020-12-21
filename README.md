# subito-it-searcher

BeautifulSoup toy example running queries and scraping results on a popular italian ad website

## The fork
This fork adds:
* Infinite refresh with adjustable delay
* Windows notifications

## Configuration
Before using this searcher, you must first install the following external modules through CLI (Windows: pip install [modulename]; Mac/Linux: sudo pip install [modulename]):
* `requests`
* `bs4` (BeautifulSoup)
* `telegram_send` (this searcher supports Telegram for notifications of new records found)

Also, this searcher is compatible with Python 3.x versions.

### telegram_send configuration
After installing the telegram_send module you must configure it, following this simple steps:
* From the CLI write `telegram-send --configure` and follow the on-screen instruction for creating the bot
* After creating the bot, from the BotFather page digit the /token command
* Next, you must copy the token and paste it on the CLI and press Enter
* Finally, you have to add your own bot to the chat list and send to the bot the password appeared on the CLI

## Usage
Write `python3 subito-searcher.py --help` for help
