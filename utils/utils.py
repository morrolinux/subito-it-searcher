import os
import json


# load from file
def load_queries(queries, dbFile):
    '''A function to load the queries from the json file'''
    if not os.path.isfile(dbFile):
        return

    with open(dbFile) as file:
        queries = json.load(file)
    return queries

def load_api_credentials(apiCredentials, telegramApiFile):
    '''A function to load the telegram api credentials from the json file'''
    if not os.path.isfile(telegramApiFile):
        return

    with open(telegramApiFile) as file:
        apiCredentials = json.load(file)
    return apiCredentials


def print_queries(queries):
    '''A function to print the queries'''
    #print(queries, "\n\n")

    for search in queries.items():
        print("\nsearch: ", search[0])
        for query_url in search[1]:
            print("query url:", query_url)
            for url in search[1].items():
                for minP in url[1].items():
                    for maxP in minP[1].items():
                        for result in maxP[1].items():
                            print("\n", result[1].get('title'), ":", result[1].get('price'), "-->", result[1].get('location'))
                            print(" ", result[0])


# printing a compact list of trackings
def print_sitrep(queries):
    '''A function to print a compact list of trackings'''
    i = 1
    for search in queries.items():
        print('\n{}) search: {}'.format(i, search[0]))
        for query_url in search[1].items():
            for minP in query_url[1].items():
                for maxP in minP[1].items():
                    print("query url:", query_url[0], " ", end='')
                    if minP[0] !="null":
                        print(minP[0],"<", end='')
                    if minP[0] !="null" or maxP[0] !="null":
                        print(" price ", end='')
                    if maxP[0] !="null":
                        print("<", maxP[0], end='')
                    print("\n")
        i+=1


# check the price of a product against a user-defined minPrice
def minPrice_check(minPrice, price):
    return True if minPrice == "null" or price == "Unknown price" or price>=int(minPrice) else False

# check the price of a product against a user-defined maxPrice
def maxPrice_check(maxPrice, price):
    return True if maxPrice == "null" or price == "Unknown price" or price<=int(maxPrice) else False