#!/usr/bin/env python3.7

import argparse
import requests
from bs4 import BeautifulSoup, Tag
import json
import os
import platform
import re
from datetime import datetime

# Set up argument parser
parser = argparse.ArgumentParser(description="Track items for sale and notify on updates.")
parser.add_argument("--add", dest='name', help="Name of new tracking to be added")
parser.add_argument("--url", help="URL for your new tracking's search query")
parser.add_argument("--minPrice", type=int, help="Minimum price for the query")
parser.add_argument("--maxPrice", type=int, help="Maximum price for the query")
parser.add_argument("--delete", help="Name of the search you want to delete")
parser.add_argument('--refresh', '-r', action='store_true', help="Refresh search results once")
parser.add_argument('--daemon', '-d', action='store_true', help="Keep refreshing search results indefinitely (default delay 120 seconds)")
parser.add_argument('--activeHour', '-ah', help="Time slot. Hour when to be active in 24h notation")
parser.add_argument('--pauseHour', '-ph', help="Time slot. Hour when to pause in 24h notation")
parser.add_argument('--delay', type=int, default=120, help="Delay for the daemon option (in seconds)")
parser.add_argument('--list', action='store_true', help="Print a list of current trackings")
parser.add_argument('--short_list', action='store_true', help="Print a more compact list")
parser.add_argument('--tgoff', action='store_true', help="Turn off Telegram messages")
parser.add_argument('--notifyoff', action='store_true', help="Turn off Windows notifications")
parser.add_argument('--addtoken', dest='token', help="Telegram setup: add bot API token")
parser.add_argument('--addchatid', dest='chatid', help="Telegram setup: add bot chat ID")

args = parser.parse_args()

# Constants
DB_FILE = "searches.tracked"
TELEGRAM_API_FILE = "telegram_api_credentials"
queries = {}
api_credentials = {}

# Windows notifications setup
if platform.system() == "Windows":
    from win10toast import ToastNotifier
    toaster = ToastNotifier()

def load_json(file_path):
    """Load JSON data from a specified file."""
    if not os.path.isfile(file_path):
        return {}
    with open(file_path) as file:
        return json.load(file)

def save_json(file_path, data):
    """Save JSON data to a specified file."""
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Load data from files
queries = load_json(DB_FILE)
api_credentials = load_json(TELEGRAM_API_FILE)

def print_queries():
    """Print the current search queries and results."""
    for search_name, search_data in queries.items():
        print(f"\nSearch: {search_name}")
        for url, price_data in search_data.items():
            for min_price, max_data in price_data.items():
                for max_price, results in max_data.items():
                    for link, details in results.items():
                        print(f"\n{details['title']} : {details['price']} --> {details['location']}")
                        print(f"Link: {link}")

def print_sitrep():
    """Print a compact list of current tracking statuses."""
    for i, (search_name, search_data) in enumerate(queries.items(), start=1):
        print(f'\n{i}) Search: {search_name}')
        for url, price_data in search_data.items():
            for min_price, max_data in price_data.items():
                for max_price, results in max_data.items():
                    price_range = f"Price: {min_price} < {max_price}" if max_price != "null" else f"Min Price: {min_price}"
                    print(f"Query URL: {url} - {price_range}")

def refresh_queries(notify):
    """Refresh the stored queries and notify if new items are found."""
    try:
        for search_name, search_data in queries.items():
            for url, price_data in search_data.items():
                for min_price, max_data in price_data.items():
                    for max_price, results in max_data.items():
                        run_query(url, search_name, notify, min_price, max_price)
    except requests.exceptions.RequestException as e:
        print(f"{datetime.now()}: ***Error occurred: {e}***")

def delete_query(to_delete):
    """Delete a specified search query."""
    queries.pop(to_delete, None)

def run_query(url, name, notify, min_price, max_price):
    """Execute a search query and check for new items."""
    print(f"{datetime.now()}: Running query (\"{name}\" - {url})...")
    products_deleted = False
    msg = []

    # Validate and sanitize the URL
    if not re.match(r'^https?://', url):
        print(f"{datetime.now()}: Invalid URL: {url}")
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    product_list_items = soup.find_all('div', class_=re.compile(r'item-card'))

    for product in product_list_items:
        title = product.find('h2').string
        try:
            price = product.find('p', class_=re.compile(r'price')).get_text(strip=True)
            price = int(price.replace('.', '')[:-2])  # Assuming price has decimals
        except Exception:
            price = "Unknown price"

        link = product.find('a')['href']
        sold = product.find('span', re.compile(r'item-sold-badge'))

        # Check if the product has already been sold
        if sold is not None:
            if link in queries.get(name, {}).get(url, {}).get(min_price, {}).get(max_price, {}):
                del queries[name][url][min_price][max_price][link]
                products_deleted = True
            continue

        try:
            location = product.find('span', re.compile(r'town')).string + product.find('span', re.compile(r'city')).string
        except Exception:
            print(f"{datetime.now()}: Unknown location for item: {title}")
            location = "Unknown location"

        if (min_price is None or price == "Unknown price" or price >= min_price) and (max_price is None or price == "Unknown price" or price <= max_price):
            if name not in queries:  # Insert the new search
                queries[name] = {url: {min_price: {max_price: {link: {'title': title, 'price': price, 'location': location}}}}}
                print(f"{datetime.now()}: New search added: {name}")
                print(f"{datetime.now()}: Adding result: {title} - {price} - {location}")
            else:  # Add search results to dictionary
                if link not in queries[name][url][min_price][max_price]:
                    queries[name][url][min_price][max_price][link] = {'title': title, 'price': price, 'location': location}
                    msg.append(f"{datetime.now()}: New element found for {name}: {title} @ {price} - {location} --> {link}")

    if msg:
        if notify:
            notify_user(msg)
        save_json(DB_FILE, queries)  # Save queries if modified
    else:
        print('\nAll lists are already up to date.')

    # Save updated queries if any products were deleted
    if products_deleted:
        save_json(DB_FILE, queries)

def notify_user(msg):
    """Send notifications to the user based on the platform."""
    if not args.notifyoff and platform.system() == "Windows":
        global toaster
        toaster.show_toast("New Announcements", f"Query: {name}")
    if is_telegram_active():
        send_telegram_messages(msg)
    print("\n".join(msg))
    print(f'\n{len(msg)} new elements have been found.')

def is_telegram_active():
    """Check if Telegram notifications are active."""
    return not args.tgoff and "chatid" in api_credentials and "token" in api_credentials

def send_telegram_messages(messages):
    """Send a list of messages to the specified Telegram chat."""
    for msg in messages:
        request_url = f"https://api.telegram.org/bot{api_credentials['token']}/sendMessage?chat_id={api_credentials['chatid']}&text={msg}"
        requests.get(request_url)

if __name__ == '__main__':
    # Check for specific commands and execute accordingly
    if args.list:
        print(f"{datetime.now()}: Printing current status...")
        print_queries()

    if args.short_list:
        print(f"{datetime.now()}: Printing quick sitrep...")
        print_sitrep()

    if args.add and args.url:
        if args.minPrice is None:
            args.minPrice = "null"
        if args.maxPrice is None:
            args.maxPrice = "null"
        run_query(args.url, args.name, notify=True, minPrice=args.minPrice, maxPrice=args.maxPrice)

    if args.refresh:
        refresh_queries(notify=True)

    if args.delete:
        delete_query(args.delete)
        save_json(DB_FILE, queries)  # Save changes after deletion
