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
parser.add_argument('--refresh', '-r', dest='refresh', action='store_true', help="refresh search results")
parser.set_defaults(refresh=False)
parser.add_argument('--list', '-l', dest='list', action='store_true', help="print a list of current trackings")
parser.set_defaults(list=False)
parser.add_argument('--short_list', dest='short_list', action='store_true', help="print a more compact list")
parser.set_defaults(short_list=False)

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


# printing a compact list of trackings
def print_sitrep():
    global queries
    i = 1
    for search in queries.items():
        print('\n{}) search: {}'.format(i, search[0]))
        for query_url in search[1]:
            print("query url:", query_url)
        i = i+1


def refresh():
    global queries
    for search in queries.items():
        for query_url in search[1]:
            run_query(query_url, search[0])


def delete(toDelete):
    global queries
    queries.pop(toDelete)


def run_query(url, name):
    print("running query (\"{}\" - {})...".format(name, url))
    global queries
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

        
    product_list_items = soup.find('div', class_='jsx-3849450822 items visible').find_all('a')
    msg = []

    for product in product_list_items:
        title = product.find('div', class_='jsx-837743620 item-key-data').find('h2').contents[0]
                
        if(product.find('div', class_='AdElements__ItemPrice--container-L2hvbWUv') is not None):
            tmp = product.find('div', class_='AdElements__ItemPrice--container-L2hvbWUv').find('h6').contents
            price = ''.join(tmp)

        else:
            price = "Unknown price"
        link = product.get('href')

        location = product.find('div', class_='AdElements__ItemDateLocation--container-L2hvbWUv').find('span').contents[0]


        if not queries.get(name):   # insert the new search
            queries[name] = {url: {link: {'title': title, 'price': price, 'location': location}}}
            print("\nNew search added:", name)
            print("Adding result:", title, "-", price, "-", location)
        else:   # add search results to dictionary
            if not queries.get(name).get(url).get(link):   # found a new element
                tmp = "New element found for "+name+": "+title+" @ "+price+" - "+location+" --> "+link+'\n'
                msg.append(tmp)
                queries[name][url][link] = {'title': title, 'price': price, 'location': location}

    if len(msg) > 0:
        telegram_send.send(messages=msg)
        print("\n".join(msg))
        print('\n{} new elements have been found.'.format(len(msg)))
        save(dbFile)
    else:
        print('\nAll lists are already up to date.')
    # print("queries file saved: ", queries)


def save(fileName):
    with open(fileName, 'w') as file:
        file.write(json.dumps(queries))


if __name__ == '__main__':

    load_from_file(dbFile)
    
    if args.list:
        print("printing current status...")
        print_queries()
    
    if args.short_list:
        print('printing quick sitrep...')
        print_sitrep()

    if args.url is not None and args.name is not None:
        run_query(args.url, args.name)

    if args.refresh:
        refresh()

    if args.delete is not None:
        delete(args.delete)

    print()
    save(dbFile)
