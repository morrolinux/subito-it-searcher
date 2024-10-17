# Improved Version of Subito-IT-Searcher

This is a BeautifulSoup scraper designed to run queries on the popular Italian ad website, Subito.it. The searcher is compatible with Python 3.x versions.

## Features
Thanks to contributions from Marco Perronet:
- **Infinite Refresh**: Adjustable delay for refreshing searches.
- **Multiplatform Support**: Works seamlessly on Windows, macOS, and Linux.
- **Windows 10 Notifications**: Receive notifications directly on your Windows machine.
- **Simplified Telegram Setup**: Easy configuration for Telegram bot notifications.
- **Connection Error Handling**: Improved stability and error handling.
- **Flooding Prevention**: Avoid excessive notifications on Telegram.

## Setup

### 1. Install Dependencies
To install the required Python libraries, run:
```bash
pip3 install -r requirements.txt
```
**Note**: Windows 10 users should also install the `win10toast` package for notifications.

### 2. Telegram Configuration
To receive updates via Telegram, follow these steps:

1. **Create a Bot**: Write to the BotFather on Telegram.
2. **Save API Key**: BotFather will provide an API key; make sure to save it.
3. **Create a Channel**: Set up a public channel and add your new bot as an administrator.
4. **Channel Name**: Save the channel name with the "@" symbol, e.g., `@subito_bot`.

To configure Telegram for your bot, invoke the script with the following command:

```bash
python3 subito-searcher.py --addtoken [YOUR_API_TOKEN] --addchatid [YOUR_CHANNEL_NAME]
```

## Usage
To see all available command-line arguments, run:

```bash
python3 subito-searcher.py --help
```

**Note**: The script always requires at least one argument to start. Here’s a quick cheatsheet for common commands:

- **Add a New Query** (name: "Auto"):
  ```bash
  python3 subito-searcher.py --add Auto --url "https://www.subito.it/annunci-italia/vendita/usato/?q=auto" --minPrice 50 --maxPrice 100
  ```
  *(Always use `--add` and `--url` together; min and max prices are optional)*

- **Remove a Query** (name: "Auto"):
  ```bash
  python3 subito-searcher.py --delete Auto
  ```

- **List All Added Queries**:
  ```bash
  python3 subito-searcher.py --short_list
  ```

- **Start the Bot**: It will search for new announcements every 2 minutes:
  ```bash
  python3 subito-searcher.py --daemon
  ```

- **Custom Delay** (e.g., 30 seconds):
  ```bash
  python3 subito-searcher.py --daemon --delay 30
  ```

- **Disable Windows Notifications**:
  ```bash
  python3 subito-searcher.py --notifyoff
  ```

- **Disable Telegram Messages**:
  ```bash
  python3 subito-searcher.py --tgoff
  ```

## Example Setup
Below is a list of commands used to set up the bot:

```bash
python3 subito-searcher.py --addtoken "YOUR_API_TOKEN" --addchatid "@subito_it_test"
python3 subito-searcher.py --add Auto --url "https://www.subito.it/annunci-italia/vendita/usato/?q=auto"
python3 subito-searcher.py --add Iphone --url "https://www.subito.it/annunci-italia/vendita/usato/?q=iphone"
python3 subito-searcher.py --add ScarpeMaxMin --url "https://www.subito.it/annunci-italia/vendita/usato/?q=scarpe" --minPrice 10 --maxPrice 150
python3 subito-searcher.py --daemon --delay 10
```
*(The token above is a placeholder and should not be used.)*

Queries like "Auto", "Iphone", and "Scarpe" are common, so you should start receiving notifications on Telegram!

To test if your bot can receive messages, use the following link (remember to replace placeholders with your token and chat ID):

```
https://api.telegram.org/bot[YOUR_BOT_TOKEN]/sendMessage?chat_id=[YOUR_CHANNEL_NAME]&text=Test Message
```

For example:
```
https://api.telegram.org/bot6168613223:oij9JDXXlipj92jDj0j90JFWO292/sendMessage?chat_id=@subito_it_test&text=Ciao
```

### Troubleshooting
- **Bot Configuration**: Ensure the bot is added to the channel and set as an administrator.
- **Correct Chat ID**: Verify you are using the correct chat ID with the "@" symbol (e.g., `@subito_it_test`).
- **Patience**: Notifications might take a few minutes to arrive. Make sure your query is common (e.g., "Auto") and consider setting a lower delay (e.g., `python3 subito-searcher.py --daemon --delay 10`) for testing.
```