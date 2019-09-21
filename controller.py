'''
Controller of Foodstitute
'''
import settings
import model
import view
import argparse
import pdb
KEYS = ['code', 'product_name', 'categories', 'nutrition_grade_fr']

def run():
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
    # history = [choose_action]
    # function, parameter = history[-1]('', db)
    choose_action('', db)

def choose_action(_, db):
    '''
    chose a basic action
    Arguments:
        _ unused
        db {database}
    '''
    question = 'What do you want?'
    answers = ['Substitute a product.', 'Manage favourites.']
    res = {
        'Substitute a product.': choose_category,
        'Manage favourites.': manage_favourites,
        'B': quit_app,
        'Q': quit_app,
    }
    choice = view.get_choice(question, answers)
    return res.get(choice)(choice, db)

def choose_category(_, db):
    '''
    Chose a category
    Arguments:
        _ unused
        db {database}
    '''
    question = 'Which category of product you want to use?'
    res = {
        'B': choose_action,
        'Q': quit_app,
    }
    choice = view.get_choice(question, model.CATEGORIES)
    # Default is choose_product, else choose_action or quit_app
    return res.get(choice, choose_product)(choice, db)

def choose_product(category, db):
    '''
    chose a category
    Arguments:
        category {string}
        db {database}
    '''
    question = 'Which product do you want to substitute?'
    products = model.Category(category).get_products(db)
    products_codes = list(zip(*products))[0]
    products_names = list(zip(*products))[1]
    res = {
        'B': choose_category,
        'Q': quit_app,
    }
    choice = view.get_choice(question, products_names)
    breakpoint()
    return res.get(choice, find_product)(products_codes[products_names.index(choice)], db)
    # return view.get_choice(question, list(zip(*products))[1])

def find_product(code, db):
    print("Choisir un meilleur produit:\n foo\n bar\n")
    save_product(code, db)

def save_product(code, db):
    print('on enregistre' + code + 'son substitut')
    print("on va dire que c'est bon")
    choose_action(code, db)

def manage_favourites(_, db):
    '''
    chose a category
    Arguments:
        _ unused
        db {database}: database
    '''
    pass

def quit_app(_, db):
    '''
    Exit app with 2 fake arguments
    '''
    exit


if __name__ == "__main__":
    run()
