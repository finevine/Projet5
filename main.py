'''
Main file for running Foodstitute
'''
import requests
from model import *
from functions_main import start, run, exit_program


def main():
    '''
    Main loop for the programme
    '''
    # First menu
    choice = start()

    while choice != 'Q':
        # Run 1 or 2
        choice = run(choice)

    # exit_program()


    search_param = {"search_terms": "candies",
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
