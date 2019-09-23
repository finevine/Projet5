'''
The model of the Physical Data model
'''
import mysql.connector
from mysql.connector import errorcode
import requests
import pdb
from getpass import getpass
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES, USER


#####################################################
#                 PRODUCT IN THE API                #
#####################################################
class Product_API:
    ''' A product from OpenFood Fact with only interesting attributes'''
    def __init__(self, product_dict):
        self.code = product_dict.get('code', 'not-applicable')
        self.name = product_dict.get('product_name', 'not-applicable')
        full_categories = product_dict.get('categories', '').lower()
        # Keep only intersection of categories and full_categories
        self.categories = list(
            set(CATEGORIES) & set(full_categories.split(','))
            )
        self.nutrition_grade = product_dict.get(
            'nutrition_grade_fr', '')

    def __repr__(self):
        categories = ''
        for cat in self.categories:
            categories += cat + ';'
        return self.name + \
            "\nCode: " + self.code + \
            "\nNutriscore: " + self.nutrition_grade + \
            "\nCategories: " + categories + "\n"

    def insert_from_API(self, db):
        connection = db.connection
        cursor = connection.cursor()
        try:
            # Product_API may have multiples categories of CATEGORIES
            for category in self.categories:
                query = (
                    'INSERT INTO Products '
                    '(code,  name, category, nutrition_grade) '
                    'VALUES (%(code)s, %(name)s, %(cat)s, %(nutrition_grade)s)'
                    )
                code = {
                    'code': self.code,
                    'name': self.name,
                    'cat': category,
                    'nutrition_grade': self.nutrition_grade
                }
                cursor.execute(query, code)

            cursor.close()
        except mysql.connector.Error as error:
            pass
            # print(f'Failed to insert record to MySQL table: {error}')


#####################################################
#                    PRODUCT IN DB                  #
#####################################################
class Product:
    ''' A class for products (row in Table Product) '''
    def __init__(self, cursor_row):
        self.code = cursor_row[0]
        self.name = cursor_row[1]
        self.category = cursor_row[2]
        self.nutrition_grade = cursor_row[3]

    def __repr__(self):
        return self.code + \
            "\nName: " + self.name + \
            "\nCategories: " + self.category + \
            "\nNutriscore: " + self.nutrition_grade

    def __gt__(self, other):
        '''
        Compare self to other with self > other in nutrition quality
        '''
        nutrition_grades = {
            'a': 5,
            'b': 4,
            'c': 3,
            'd': 2,
            'e': 1,
        }
        return nutrition_grades[self.nutrition_grade] > \
            nutrition_grades[other.nutrition_grade]
    

#####################################################
#                    FAVOURITE IN DB                #
#####################################################
class Favourite:
    ''' A class for saved products '''
    def __init__(self, code_healthy):
        super().__init__()
        # code_healthy is the code of the substitute
        self.code_substitute = code_healthy


#####################################################
#                    A CATEGORY                     #
#####################################################
class Category:
    ''' Class for one of the categories to analyse '''
    def __init__(self, cat_name):
        self.name = cat_name

    def search_param(self, page):
        ''' change search param depending on category and page
        Arguments:
            page {int} -- page of READ API request
        '''
        search_param = {"search_terms": ", " + self.name + ",",
                        "search_tag": "categories_tag",
                        "sort_by": "unique_scans_n",
                        "page_size": 1000,
                        "json": 1,
                        "page": page}
        return search_param

    def get_api_products(self):
        ''' This function get the products of a category
        and return them as a list of Product_API '''
        # list of product to output
        products = []
        # initialize to page 1 of search result
        page = 1
        req = requests.get(
            API_URL,
            params=self.search_param(page),
            headers=SEARCH_HEADER)
        # output of request as a json file
        req_output = req.json()
        # list of product of the output
        products_output = req_output['products']
        # store product classes
        for product in products_output:
            products.append(Product_API(product))

        # then increment page to search next page of results
        while products_output:
            page += 1
            req = requests.get(
                API_URL,
                params=self.search_param(page),
                headers=SEARCH_HEADER)
            req_output = req.json()
            products_output = req_output['products']

            for product in products_output:
                products.append(Product_API(product))
        return products


#####################################################
#                    THE DATABASE                   #
#####################################################
class DataBase:
    ''' Database class '''
    # essayer d'hériter de connection.MySQLConnection()
    def __init__(self, MDP):
        try:
            # user_password = getpass('Database password? ')
            user_db = mysql.connector.connect(
                host="localhost",
                user=USER,
                password=MDP,
                database="foodstitute",
                auth_plugin='mysql_native_password'
                )
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            # Connect to DB
            self.connection = user_db

    def create_tables(self):
        ''' Function to initialize the database
        Arguments:
            None'''
        # store tables creations in a dictionnary
        TABLES = {}
        TABLES['Products'] = (
            """CREATE TABLE Products (
                code VARCHAR(13) NOT NULL,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(40) NOT NULL,
                nutrition_grade VARCHAR(1) NOT NULL,
                PRIMARY KEY (code, category)
                )
                ENGINE=InnoDB;
            """)

        TABLES['Favourites'] = (
            """CREATE TABLE Favourites (
                code_unhealthy VARCHAR(13) NOT NULL REFERENCES Products(code),
                code_healthy VARCHAR(13) NOT NULL REFERENCES Products(code),
                category VARCHAR(40) NOT NULL REFERENCES Products(category),
                PRIMARY KEY (code_healthy, code_unhealthy, category)
                )
            ENGINE=InnoDB;
            """)

        # Open cursor linked to DB (self)
        connection = self.connection
        cursor = connection.cursor()

        # Create tables
        for table_name in TABLES:
            table_creation = TABLES[table_name]
            try:
                print(f'Creating table {table_name}: ', end='')
                cursor.execute(table_creation)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        # Close cursor
        cursor.close()

    def feed_database(self, category):
        ''' Method to feed the database
        Arguments:
            category {Category}'''
        # get product from category
        products_list = category.get_api_products()

        for product in products_list:
            if product.categories and product.nutrition_grade:
                product.insert_from_API(self)
        print('Inserted in database: ' + category.name)

    def drop_Products(self):
        '''
        DROP TABLE Products
        '''
        connection = self.connection
        cursor = connection.cursor()
        query = ("DROP TABLE IF EXISTS Products ")
        cursor.execute(query)
        cursor.close()

    def get_products(self, category):
        '''
        Get Products that are in Category in the DB
        Arguments:
            category {string}
        '''
        connection = self.connection
        cursor = connection.cursor()
        query = (
            "SELECT * FROM Products "
            "WHERE category = %(cat)s"
            )
        parameter = {'cat': category}
        cursor.execute(query, parameter)
        # products = cursor.fetchall()
        return [Product(prod) for prod in cursor]
        cursor.close()

    def find_healthier(self, product):
        '''
        Find healthier product
        Arguments:
            product {Product}
        '''
        healthier_products = []
        # get product from the same category
        products_of_cat = self.get_products(product.category)
        for product_of_cat in products_of_cat:
            # for each check if healthier
            if product_of_cat > product:
                healthier_products.append(product_of_cat)
        return healthier_products


    def save_favourite(self, product, substitute):
        ''' save a product substituted as favourite
        Arguments:
            product, substitute {Product}
        '''
        connection = self.connection
        cursor = connection.cursor()
        try:
            query = (
                    'INSERT INTO Favourites '
                    '(code_unhealthy, code_healthy, category) '
                    'VALUES (%(code_product)s, %(code_substitute)s, %(cat)s)'
            )
            code = {
                    'code_product': product.code,
                    'code_substitute': substitute.code,
                    'cat': product.category
            }
            cursor.execute(query, code)
            cursor.close()
            # Commit changes
            connection.commit()
            # Finally close connection
            connection.close()
        except mysql.connector.Error as error:
            print(f'Failed to insert Favourite to MySQL table: {error}')
