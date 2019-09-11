'''
The model of the Physical Data model
'''
import mysql.connector
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
        #self.categories = product.get('categories', 'not-applicable')
        #self.categories = (full_categories).split(',')
        #self.categories = CATEGORIES
        # Keep only intersection of categories and full_categories
        self.categories = list(set(CATEGORIES) & set(full_categories.split(',')))
        if self.categories != []:
            while len(self.categories) < len(CATEGORIES):
                self.categories.append('')
        self.nutrition_grade = product.get(
            'nutrition_grade_fr', '')

    def __repr__(self):
        categories = ''
        for cat in self.categories:
            categories += cat + ';'
        return self.name+\
            "\nCode: "+self.code+\
            "\nNutriscore: "+self.nutrition_grade+\
            "\nCategories: "+categories

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
            code = self.code
            cursor.execute(query, code)
            categories = cursor.fetchall()

            query = (
                """SELECT nutrition_grade
                FROM Products
                WHERE code = %s""")
            code = self.code
            cursor.execute(query, code)
            nutrition_grade = cursor.fetchall()
            cursor.close()
            return (categories, nutrition_grade)
        except mysql.connector.Error as error:
            print(f'Failed to get record from MySQL table: {error}')

    def insert(self, db):
        cursor = db.connection.cursor()
        try:
            query = (
                """INSERT INTO Products
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")
            cat1, cat2, cat3, cat4, cat5 = self.categories
            code = (self.code, self.name,
                    cat1, cat2, cat3, cat4, cat5,
                    self.nutrition_grade)
            cursor.execute(query, code)
            cursor.close()
        except mysql.connector.Error as error:
            print(f'Failed to insert record to MySQL table: {error}')


##################################################
class Favourite(Product):
    ''' A class for saved products '''
    def __init__(self, code_unhealthy, code_healthy):
        super().__init__(code_unhealthy, code_healthy)
        # code substitute is the code of the product that it substitute
        self.code_unhealthy = code_unhealthy
        self.code_healthy = code_healthy


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
        search_param = {"search_terms": self.name,
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
        while products_output != []:
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


##################################################
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
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            # Connect to DB
            self.connection = user_db

    def close(self):
        self.close()

    def create_tables(self):
        ''' Function to initialize the database
        Arguments:
            None'''
        # store tables creations in a dictionnary
        TABLES = {}
        TABLES['Products'] = (
            """CREATE TABLE Products (
                code VARCHAR(13) NOT NULL,
                name VARCHAR(40) NOT NULL,
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
                code_healthy VARCHAR(13) NOT NULL,
                code_unhealthy VARCHAR(13) NOT NULL,
                PRIMARY KEY (code_healthy, code_unhealthy)
                )
            ENGINE=InnoDB;
            """)

        # TABLES['Favourites'] = (
        #     """CREATE TABLE Favourites (
        #         code_healthy VARCHAR(13) NOT NULL,
        #         code_unhealthy VARCHAR(13) NOT NULL,
        #         PRIMARY KEY (code_healthy, code_unhealthy),
        #         FOREIGN KEY (code_healthy, code_unhealthy)
        #             REFERENCES (Produts(code), Produts(code))
        #         )
        #     ENGINE=InnoDB;
        #     """)
        
        # Open cursor linked to DB (self)
        connection = self.connection
        cursor = connection.cursor()

        #Create tables
        for table_name in TABLES:
            table_creation = TABLES[table_name]
            try:
                print(f'Creating table {table_name}: ', end='')
                cursor.execute(table_creation)
            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")    
        #Close cursor
        cursor.close()
    
    def feed_database(self, category):
        ''' Method to feed the database
        Arguments:
            category {Category}'''
        # get product from category
        products_list = category.get_api_products()

        for product in products_list:
            if product.categories != [] and product.nutrition_grade != []:
                product.insert(self)
        print('Database ready to go!')
