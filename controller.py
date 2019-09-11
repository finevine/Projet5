'''
Controller of Foodstitute
'''
import mysql.connector
import requests
from getpass import getpass
# from mysql.connector import errorcode
from model import Category, Product, Favourite
from settings import API_URL, SEARCH_HEADER, DATABASE, CATEGORIES


def create_table():
    ''' create a table in the db '''
    pass


def close_connection(connection):
    ''' close close_connection '''
    connection.close()


def compare_products(code_product):
    ''' compare 2 products of the database'''
    # trier par catégories dans les 10 premiers méthode de produits
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
