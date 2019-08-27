'''
The model of the Physical Data model
'''
import mysql.connector
import requests
from getpass import getpass
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES, USER


class Category:
    ''' Class for one of the categories to analyse '''
    def __init__(self, cat_id, cat_name):
        self.id = cat_id
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


class Product:
    ''' A product from OpenFood Fact with only interesting attributes'''
    def __init__(self, product):
        self.code = product.get('code', 'not-applicable')
        self.name = product.get('product_name', 'not-applicable')
        self.categories = product.get('categories', 'not-applicable')
        self.nutrition_grade = product.get('nutrition_grade_fr', 'not-applicable')
    

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


class Table:
    ''' represent a generic Table

    Arguments: