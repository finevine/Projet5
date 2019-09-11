'''
Main file for running Foodstitute
'''
import requests
from model import *


def main():
    products = Category('nuts').get_api_products()
    print(products[1])
    print(products[2])
    print(products[3])

def main2(): 
    db = DataBase()
    db.create_tables()
    db.feed_database(Category('candies'))
    db.connection.commit()
    db.connection.close()

if __name__ == "__main__":
    main2()
