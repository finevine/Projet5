'''
Controller of Foodstitute
'''
import settings
import model
import view
import argparse
import pdb


def choose_action():
    question = 'What do you want?'
    answer = ['Substitute a product.', 'Manage favourites.']
    return view.get_choice(question, answer, 0)

def choose_category():
    question = 'Which category of product you want to use?'
    return view.get_choice(question, model.CATEGORIES, 1)

def choose_product(category, db):
    question = 'Which product do you want to substitute?'
    products = model.Category(category).get_products(db)
    breakpoint()
    return view.get_choice(question, list(zip(*products))[1], 2)


def run():
    step = 0
    choice = ''
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

    view.start_view()
    while step >= 0:
        if step == 0:
            choice, step = choose_action()
        elif step == 1:
            choice, step = choose_category()
        elif step == 2:
            # breakpoint()
            choice, step = choose_product(choice, db)
        print(choice, 'step', step)


if __name__ == "__main__":
    run()
