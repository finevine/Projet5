'''
The model of the Physical Data model
'''
import mysql.connector
from mysql.connector import errorcode
import requests
from getpass import getpass
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES, USER


##################################################
class Product:
    ''' A product from OpenFood Fact with only interesting attributes'''
    def __init__(self, product):
        self.code = product.get('code', 'not-applicable')
        self.name = product.get('product_name', 'not-applicable')
        full_categories = product.get('categories', '').lower()
        # Keep only intersection of categories and full_categories
        self.categories = list(
            set(CATEGORIES) & set(full_categories.split(','))
            )
        if self.categories:
            while len(self.categories) < len(CATEGORIES):
                self.categories.append('')
        self.nutrition_grade = product.get(
            'nutrition_grade_fr', '')

    def __repr__(self):
        categories = ''
        for cat in self.categories:
            categories += cat + ';'
        return self.name + \
            "\nCode: " + self.code + \
            "\nNutriscore: " + self.nutrition_grade + \
            "\nCategories: " + categories + "\n"

    def find_characteristics(self, db):
        ''' Find categories of a product in the DB
        Arguments :
            connection {sql connection}
        '''
        try:
            cursor = db.connection.cursor()
            query = (
                """SELECT category1, category2, category3, category4, category5
                FROM Products
                WHERE code = %s""")
            code = (self.code,)
            cursor.execute(query, code)
            categories = [line for line in cursor]
            # A VOIR SI ÇA MARCHE OU FETCHALL

            query = (
                """SELECT nutrition_grade
                FROM Products
                WHERE code = %s""")
            code = (self.code,)
            cursor.execute(query, code)
            nutrition_grade = cursor.fetchall()
            cursor.close()
            return (categories, nutrition_grade)
        except mysql.connector.Error as error:
            print(f'Failed to get record from MySQL table: {error}')

    def insert_into(self, db):
        connection = db.connection
        cursor = connection.cursor()
        try:
            # This query uses a dictionnary
            query = (
                'INSERT INTO Products '
                '(code,  name, '
                'category1, category2, category3, category4, category5, '
                'nutrition_grade) '
                'VALUES (%(code)s, %(name)s, '
                '%(cat1)s, %(cat2)s, %(cat3)s, %(cat4)s, %(cat5)s, '
                '%(nutrition_grade)s)'
                )
            code = {
                'code': self.code,
                'name': self.name,
                'cat1': self.categories[0],
                'cat2': self.categories[1],
                'cat3': self.categories[2],
                'cat4': self.categories[3],
                'cat5': self.categories[4],
                'nutrition_grade': self.nutrition_grade
            }
            cursor.execute(query, code)

            cursor.close()
        except mysql.connector.Error as error:
            pass
            # print(f'Failed to insert record to MySQL table: {error}')


##################################################
class Favourite(Product):
    ''' A class for saved products '''
    def __init__(self, code_unhealthy, code_healthy):
        super().__init__(code_unhealthy, code_healthy)
        # code substitute is the code of the product that it substitute
        self.code_unhealthy = code_unhealthy
        self.code_healthy = code_healthy

    def save_favourite(code_product):
        ''' save a product substituted as favourite '''
        # compare_product(code_product)
        pass


##################################################
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
        and return them as a list '''
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
            products.append(Product(product))

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
                products.append(Product(product))
        return products

    def get_products(self, db):
        '''
        Get Products that are in Category in the DB
        Arguments:
            db {Database}
        '''
        cursor = db.connection.cursor()
        query = (
            "SELECT * FROM Products "
            "WHERE category1 = %(cat)s "
            "OR category2 = %(cat)s "
            "OR category3 = %(cat)s "
            "OR category4 = %(cat)s "
            "OR category5 = %(cat)s"
            )
        parameter = {'cat': self.name}
        cursor.execute(query, parameter)
        products = cursor.fetchall()
        print(products)
        cursor.close()


##################################################
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
                category1 VARCHAR(40) NOT NULL,
                category2 VARCHAR(40),
                category3 VARCHAR(40),
                category4 VARCHAR(40),
                category5 VARCHAR(40),
                nutrition_grade VARCHAR(1) NOT NULL,
                PRIMARY KEY (code)
                )
                ENGINE=InnoDB;
            """)

        TABLES['Favourites'] = (
            """CREATE TABLE Favourites (
                code_healthy VARCHAR(13) NOT NULL REFERENCES Products(code),
                code_unhealthy VARCHAR(13) NOT NULL REFERENCES Products(code),
                PRIMARY KEY (code_healthy, code_unhealthy)
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
                product.insert_into(self)
        print('Inserted in database: ' + category.name)
