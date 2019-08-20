'''
Main file for running Foodstitute
'''
import requests
from model import *
from functions_main import start, choose_category, manage_personnal_food


def main():
    '''
    Main loop for the programme
    '''
    categories = ['breakfast-cereals',
                  'candies',
                  'dark-chocolates',
                  'ice-creams-and-sorbets',
                  'nuts']

    # First menu
    first_choice = start()

    if first_choice == 1:
        second_choice = choose_category(categories)
    else:
        second_choice = manage_personnal_food()

    search_param = {"search_terms": categories[second_choice],
                    "search_tag": "categories",
                    "sort_by": "unique_scans_n",
                    "page_size": 20,
                    "json": 1,}
    search_header = {"user-agent": "Foodstitute - https://github.com/finevine/Projet5"}
    req = requests.get("https://fr-en.openfoodfacts.org/cgi/search.pl?",
                       params=search_param, headers=search_header)
    results = req.json()
    print(results.keys())
    print(results["products"][0]["product_name_fr"])
    print(req.url)


if __name__ == "__main__":
    main()
