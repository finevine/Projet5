'''
Setup of Foodstitute
'''
from model import *
from functions_setup import init_prod_db


def main():
    '''
    Main loop for the program
    '''
    print(init_prod_db())


if __name__ == "__main__":
    main()
