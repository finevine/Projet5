'''
Controller of Foodstitute
'''
import mysql.connector
import requests
from getpass import getpass
# from mysql.connector import errorcode
from model import Category, Product, Favourite
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES



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
    ''' function to initialize the database '''
    DB_NAME = 'foodstitude'
    # store tables creations in a dictionnary
    TABLES = {}
    TABLES['MainCategories'] = (
        """CREATE TABLE MainCategories (
            id SMALLINT NOT NULL AUTO_INCREMENT,
            name VARCHAR(40) NOT NULL,
            PRIMARY KEY (id)
            )
            ENGINE=InnoDB;
        """)

    TABLES['products'] = (
        """CREATE TABLE MainCategories (
            code VARCHAR(13) NOT NULL,
            product_name name VARCHAR(40) NOT NULL,
            PRIMARY KEY (code)
            )
            ENGINE=InnoDB;
        """)

    TABLES['favourites'] = (
        """CREATE TABLE MainCategories (
            id SMALLINT NOT NULL AUTO_INCREMENT,
            name VARCHAR(40) NOT NULL,
            PRIMARY KEY (id)
            )
        ENGINE=InnoDB;
        """)

    for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    cnx.close()
    


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
    print(get_api_products('candies'))
