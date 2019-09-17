API_URL = 'https://fr-en.openfoodfacts.org/cgi/search.pl?'
SEARCH_PARAM = {"search_terms": {},
                "search_tag": "categories",
                "sort_by": "unique_scans_n",
                "page_size": 1000,
                "json": 1}
USER = 'vft'
SEARCH_HEADER = {
    "user-agent": "Foodstitute - https://github.com/finevine/Projet5"
    }
DATABASE = 'foodstitute'
CATEGORIES = [
    'meats',
    'seafood',
    'chocolates',
    'compotes',
    'nuts'
    ]
