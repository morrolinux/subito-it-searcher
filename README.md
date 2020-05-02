# subito-it-searcher

BeautifulSoup toy example running queries and scraping results on a popular italian ad website

    Configuration
Before use this searcher, you must first install the following external modules through CLI (Windows: pip install [modulename]; Mac/Linux: sudo pip install [modulename]):
    1) requests;
    2) bs4 (BeautifulSoup);
    3) telegram_send (this searcher supports Telegram for notifications of new records found).
Also, this searcher is compatible with Python 3.x versions.

    telegram_send module configuration
After installing the telegram_send module you must configure it, following this simple steps:
    1) from the CLI write "telegram_send --configure" and follow the on-screen instruction for creating the bot;
    2) after creating the bot, from the BotFather page digit the /token command;
    3) next, you must copy the token and paste it on the CLI and press Enter;
    4) finally, you have to add your own bot to the chat list and send to the bot the password appeared on the CLI.
