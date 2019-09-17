'''
Setup of Foodstitute
'''
import settings
import model
import argparse
from settings import USER


def main():
    '''
    Main function of setup.py
    It fills the tables with products of CATEGORIES in settings.py
    Arguments:
        Pass {string}: password of foodstitute
    '''
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "Pass",
        help="Password of the SQL DB foodstitute for the account" +
        USER
        )
    # Get args
    args = parser.parse_args()
    # Define password
    Pass = args.Pass
    # Connect to DB
    db = model.DataBase(Pass)
    # Create Tables
    db.create_tables()
    for category in settings.CATEGORIES:
        db.feed_database(model.Category(category))
    # Commit changes
    db.connection.commit()
    # Finally close connection
    db.connection.close()


if __name__ == "__main__":
    main()
