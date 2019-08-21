'''
Setup of Foodstitute
'''
from model import *
from functions_setup import connect_client, init_prod_db


def main():
    '''
    Main loop for the program
    '''
    user_db = connect_client()


if __name__ == "__main__":
    main()
