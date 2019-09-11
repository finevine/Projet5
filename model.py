'''
The model of the Physical Data model
'''
import mysql.connector
import requests
from getpass import getpass
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES, USER


class Category:
    ''' Class for one of the categories to analyse '''
    def __init__(self, cat_name):
        self.name = cat_name

    def search_param(self, page):
        ''' change search param depending on category and page
        Arguments:
            page {int} -- page of READ API request
        '''
        search_param = {"search_terms": self.name,
                        "search_tag": "categories",
                        "sort_by": "unique_scans_n",
                        "page_size": 1000,
                        "json": 1,
                        "page": page}
        return search_param

    def get_api_products(self):
        ''' This function get the products of a category and return them as a list '''
        # list of product to output
        products = []
        # initialize to page 1 of search result
        page = 1
        req = requests.get(API_URL, params=search_param(self, page), headers=SEARCH_HEADER)
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
            req = requests.get(API_URL, params=search_param(self, page), headers=SEARCH_HEADER)
            req_output = req.json()
            products_output = req_output['products']

            for product in products_output:
                products.append(Product(product))
        
        return products


class Product:
    ''' A product from OpenFood Fact with only interesting attributes'''
    def __init__(self, product):
        self.code = product.get('code', 'not-applicable')
        self.name = product.get('product_name', 'not-applicable')
        self.categories = product.get('categories', 'not-applicable')
        self.nutrition_grade = product.get('nutrition_grade_fr', 'not-applicable')

    def search_product(self, connection):
        ''' Find categories of a product in the DB 
        Arguments :
            connection {sql connection}
        '''
        cursor = connection.cursor()
        query = ("SELECT categories FROM products "
        "WHERE code == %s")
        code = self.code
        cursor.execute(query, code)
        
        # result = [categories for categories in cursor] # FAIRE UNE JOINTURE


class Favourite(Product):
    ''' A class for saved products '''
    def __init__(self, code_unhealthy, code_healthy):
        super().__init__(code_unhealthy, code_healthy)
        # code substitute is the code of the product that it substitute
        self.code_unhealthy = code_unhealthy
        self.code_healthy = code_healthy


class DataBase:
    ''' Database class '''
    def __init__(self):
        try:
            user_password = getpass('Database password? ')
            user_db = mysql.connector.connect(
                host="localhost",
                user=USER,
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

    def init_prod_db(categories):
        ''' function to initialize the database '''
        DB_NAME = 'foodstitude'
        # store tables creations in a dictionnary
        TABLES = {}
        TABLES['ProductsCategories'] = (
            """CREATE TABLE ProductsCategories (
                code VARCHAR(13) NOT NULL,
                category VARCHAR(40),
                PRIMARY KEY (code, category)
                )
                ENGINE=InnoDB;
            """)

        TABLES['Products'] = (
            """CREATE TABLE Products (
                code VARCHAR(13) NOT NULL,
                product_name name VARCHAR(40) NOT NULL,
                nutrition_grade VARCHAR(1) NOT NULL,
                PRIMARY KEY (code)
                )
                ENGINE=InnoDB;
            """)

        TABLES['Favourites'] = (
            """CREATE TABLE Favourites (
                code_healthy VARCHAR(13) NOT NULL,
                code_unhealthy VARCHAR(13) NOT NULL,
                PRIMARY KEY (code_healthy, code_unhealthy)
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
    
    def feed_database(products):


class Table:
    ''' represent a generic Table

    Arguments: