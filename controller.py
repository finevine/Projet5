'''
Controller of Foodstitute
'''
import mysql.connector
from getpass import getpass
from mysql.connector import errorcode
from settings import API_URL, SEARCH_HEADER, SEARCH_PARAM, DATABASE, CATEGORIES


if __name__ == "__main__":
    print('Controller used in Foodstitute')


def init_db():
    ''' initialize database '''
    pass


def compare_products(code_product):
    ''' compare 2 products of the database'''
    # trier par catégories dans les 10 premiers
    pass
    # return product


def save_favourite(code_product):
    ''' save a product substituted as favourite '''
    # compare_product(code_product)
    pass


def connect_client():
    ''' Initialize the product database '''
    # Check for existing user
    existing_user = input(
        'Do you have access to the MySql Client (Y)es/(N)o: '
        ).upper()

    if existing_user == 'N':
        # print('Let\'s create one!')
        print(
            'Please contact your Mysql admin to get \
            an access to `foodstitute` Database'
            )
        return False

    # Grant user for login and password
    user_login = input('Database login? ')
    user_password = getpass('Database password? ')

    ''' Difficult to connect as root and then as user
    if existing_user == 'N':
        statement = "CREATE USER '" + login + "'@'localhost' IDENTIFIED BY '" + password + "';"'''
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


def create_table():
    ''' create a table in the db '''
    pass


def init_prod_db(categories):
    pass


def close_connection(connection):
    ''' close close_connection '''
    connection.close()
