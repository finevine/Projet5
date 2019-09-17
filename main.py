'''
Main file for running Foodstitute
'''
import requests
import pdb
import argparse
import model
import settings


def main():
    products = Category('nuts').get_api_products()
    print(products[1])
    print(products[2])
    print(products[3])


def SELECT_EXAMPLE():
    db = DataBase()
    cursor = db.connection.cursor()
    query = ("SELECT code FROM Products WHERE code = %s")
    parameter = ('8435177055515',)
    cursor.execute(query, parameter)
    nutrition_grade = cursor.fetchall()
    print(nutrition_grade)
    cursor.close()


def main3():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "Pass",
        help="Password of the SQL DB foodstitute for the account" +
        settings.USER
        )
    # Get args
    args = parser.parse_args()
    # Define password
    Pass = args.Pass
    # Connect to DB
    db = model.DataBase(Pass)
    model.Category('seafood').get_products(db)


if __name__ == "__main__":
    main3()
