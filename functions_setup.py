'''
Functions used in Foodstitute
'''
import mysql.connector
from getpass import getpass


if __name__ == "__main__":
    print('Functions used in Foodstitute')


def connect_client():
    '''
    Initialize the product database
    '''
    # Check for existing user
    existing_user = input('Do you have access to the MySql Client (Y)es/(N)o: ').upper()

    if existing_user == 'N':
        # print('Let\'s create one!')
        print('Please contact your mmysql admin to get an access to `foodstitute` Database')
        return False

    # Grant user for login and password
    user_login = input('Database login? ')
    user_password = getpass('Database password? ')

    ''' Difficult to connect as root and then as user
    if existing_user == 'N':
        statement = "CREATE USER '" + login + "'@'localhost' IDENTIFIED BY '" + password + "';"
    '''

    # Connect to DB
    user_db = mysql.connector.connect(
        host="localhost",
        user=user_login,
        password=user_password,
        database="foodstitute",
        auth_plugin='mysql_native_password'
        )

    return user_db


def init_prod_db(categories):