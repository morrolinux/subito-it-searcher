#!/usr/bin/env python3.7

import argparse
import requests
from bs4 import BeautifulSoup
import json
import os.path
import telegram_send

parser = argparse.ArgumentParser()
parser.add_argument("--name", "--add", dest='name', help="name of new tracking to be added")
parser.add_argument("--url", help="url for your new tracking's search query")
parser.add_argument("--delete", help="name of the search you want to delete")
parser.add_argument('--refresh', dest='refresh', action='store_true', help="refresh search results")
parser.set_defaults(refresh=False)
parser.add_argument('--list', dest='list', action='store_true', help="print a list of current trackings")
parser.set_defaults(list=False)

args = parser.parse_args()

queries = dict()
dbFile = "searches.tracked"


# load from file
def load_from_file(fileName):
    global queries
    if not os.path.isfile(fileName):
        return

    with open(fileName) as file:
        queries = json.load(file)


def print_queries():
    global queries
    #print(queries, "\n\n")
    for search in queries.items():
        print("\nsearch: ", search[0])
        for query_url in search[1]:
            print("query url:", query_url)
            for url in search[1].items():
                for result in url[1].items():
                    print("\n", result[1].get('title'), ":", result[1].get('price'), "-->", result[1].get('location'))
                    print(" ", result[0])


def refresh():
    global queries
    for search in queries.items():
        for query_url in search[1]:
            run_query(query_url, search[0])


def delete(toDelete):
    global queries
    queries.pop(toDelete)


def run_query(url, name):
    print("running query ", name, url)
    global queries
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    products_list = soup.find(class_='items_listing')
    product_list_items = products_list.find_all(class_='item_list_inner')
    msg = []

    for product in product_list_items:
        desc = product.find(class_='item_description')
        title = desc.find('a').contents[0]
        if(desc.find(class_='item_price') is not None):
            price = desc.find(class_='item_price').contents[0]
        else:
            price = "Unknown price"
        link = desc.find('a').get('href')
        location = desc.find(class_="item_location").contents[0]

        if not queries.get(name):   # insert the new search
            queries[name] = {url: {link: {'title': title, 'price': price, 'location': location}}}
            print("\nNew search added:", name)
            print("Adding result:", title, "-", price, "-", location)
        else:   # add search results to dictionary
            if not queries.get(name).get(url).get(link):   # found a new element
                tmp = "New element found for "+name+": "+title+" @ "+price+" - "+location+" --> "+link
                msg.append(tmp)
                queries[name][url][link] = {'title': title, 'price': price, 'location': location}

    if len(msg) > 0:
        telegram_send.send(messages=msg)
        print("\n".join(msg))
        save(dbFile)
    # print("queries file saved: ", queries)


def save(fileName):
    with open(fileName, 'w') as file:
        file.write(json.dumps(queries))


if __name__ == '__main__':

    load_from_file(dbFile)
    
    if args.list:
        print("printing current status...")
        print_queries()

    if args.url is not None and args.name is not None:
        run_query(args.url, args.name)

    if args.refresh:
        refresh()

    if args.delete is not None:
        delete(args.delete)

    print()
    save(dbFile)
