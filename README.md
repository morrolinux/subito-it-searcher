# Improved version of subito-it-searcher

BeautifulSoup scraper running queries on a popular italian ad website.
This searcher is compatible with Python 3.x versions.

Features (thanks to Marco Perronet)
* Infinite refresh with adjustable delay
* Multiplatform support: can run also on Windows
* Windows 10 notifications
* Easier Telegram setup
* Handle connection errors
* Fix flooding on Telegram

## Setup

### Install dependencies 
```pip3 install -r requirements.txt```

NB: For Windows 10 users, install also ```win10toast```.

### Telegram configuration
To have to bot send you updates on Telegram, follow these steps:
1) Create a bot by writing to the BotFather on Telegram
2) BotFather will give you an API key: **save this API key for later**
3) Create a public channel and add the newly created bot as administrator
4) **Save the name of the channel** including the "@", for example: @subito_bot

To configure Telegram, simply invoke the script with the proper parameters as following:

`python3 subitosearcher.py --addtoken [YOUR_API_TOKEN] --addchatid [YOUR_CHANNEL_NAME]`

## Usage
Write `python3 subitosearcher.py --help` to see all the command line arguments. Keep in mind that the script *always* needs some argument in order to start. 

Here is a cheatsheet of the most common usages:

* Add a new query with name "Auto":
`python3 subitosearcher.py --add Auto --url https://www.subito.it/annunci-italia/vendita/usato/?q=auto --minPrice 50 --maxPrice 100`
(keep in mind that you *always* use `--add` and `--url` together, min and max prices are optional)

* Remove the query "Auto":
`python3 subitosearcher.py --delete Auto`

* See a list of all your added queries:
`python3 subitosearcher.py --short_list`

* **Start the bot**, it will search for new announcements every 2 minutes:
`python3 subitosearcher.py --daemon`

* Start the bot with a custom delay (example, 30 seconds):
`python3 subitosearcher.py --daemon --delay 30`

* Start the bot, but disable windows notifications:
`python3 subitosearcher.py --notifyoff`

* Start the bot, but disable telegram messages:
`python3 subitosearcher.py --tgoff`

## Example setup

Here is the list of commands I types to set up the bot on my computer:
```
python3 subitosearcher.py --addtoken "6168613223:oij9JDXXlipj92jDj0j90JFWO292" --addchatid "@subito_it_test"
python3 subitosearcher.py --add Auto --url https://www.subito.it/annunci-italia/vendita/usato/\?q\=auto
python3 subitosearcher.py --add Iphone --url https://www.subito.it/annunci-italia/vendita/usato/\?q\=iphone
python3 subitosearcher.py --add ScarpeMaxMin --url https://www.subito.it/annunci-italia/vendita/usato/\?q\=auto --minPrice 10 --maxPrice 150
python3 subitosearcher.py --daemon --delay 10
```
(Of course the token I showed here is not the real one)

"Auto", "Iphone", and "Scarpe" are very common queries, so hopefully you should see some notifications on Telegram!

If you want to check if your bot is able to receive messages, you can use this link to send a test message: https://api.telegram.org/bot[bot_token_code]/sendMessage?chat_id=[chat_id_code]&text=prova (please use your token and chat id in the link).

For example, I used: https://api.telegram.org/6168613223:oij9JDXXlipj92jDj0j90JFWO292/sendMessage?chat_id=@subito_it_test&text=Ciao

### Troubleshooting

* Did you add the bot to the channel and set it as admin?
* Did you use the correct chat id? Don't forget the "@" at the beginning (e.g. `@subito_it_test`)
* Be patient! Maybe it will take a few minutes to receive notifications. Did you use a common query where people post announcments like "Auto"? For testing, try also setting a low delay (e.g. `python3 subitosearcher.py --daemon --delay 10`)
