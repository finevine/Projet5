'''
Controller of Foodstitute
'''
import mysql.connector
import requests
from getpass import getpass
from mysql.connector import errorcode
from model import Category, Product, Favourite
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES


def connect_client():
    ''' Initialize the product database '''
    # Check for existing user
    existing_user = input(
        'Do you have access to the MySql Client (Y)es/(N)o: '
        ).upper()

    if existing_user == 'N':
        print(
            'Please contact your Mysql admin to get \
            an access to `foodstitute` Database'
            )
        return False

    # Grant user for login and password
    user_login = input('Database login? ')
    user_password = getpass('Database password? ')

    try:
        user_db = mysql.connector.connect(
            host="localhost",
            user=user_login,
            password=user_password,
            database="foodstitute",
            auth_plugin='mysql_native_password'
            )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        # Connect to DB
        return user_db


def search_param(category, page):
    ''' change search param depending on category and page '''
    search_param = {"search_terms": category,
                    "search_tag": "categories",
                    "sort_by": "unique_scans_n",
                    "page_size": 1000,
                    "json": 1,
                    "page": page}
    return search_param


def get_api_products(category):
    ''' This function get the products of a category and return them as a list '''
    # list of product to output
    products = []
    # initialize to page 1 of search result
    page = 1
    req = requests.get(API_URL, params=search_param(category, page), headers=SEARCH_HEADER)
    # output of request as a json file
    req_output = req.json()
    # list of product of the output
    products_output = req_output['products']
    # store product classes
    for product in products_output:
        products.append(Product(product))

    # then increment page to search next page of results
    while products_output != []:
        page += 1
        req = requests.get(API_URL, params=search_param(category, page), headers=SEARCH_HEADER)
        req_output = req.json()
        products_output = req_output['products']

        for product in products_output:
            products.append(Product(product))
    
    return products


def create_table():
    ''' create a table in the db '''
    pass


def init_prod_db(categories):
    pass


def close_connection(connection):
    ''' close close_connection '''
    connection.close()


def compare_products(code_product):
    ''' compare 2 products of the database'''
    # trier par catégories dans les 10 premiers
    pass
    # return product


def save_favourite(code_product):
    ''' save a product substituted as favourite '''
    # compare_product(code_product)
    pass



if __name__ == "__main__":
    print('Controller used in Foodstitute')
    # test_api('candies')
    get_api_products('candies')
