'''
Controller of Foodstitute
'''
import settings
import model
import view
import argparse
import pdb
KEYS = ['code', 'product_name', 'categories', 'nutrition_grade_fr']


#####################################################
#                  RUN & CHOOSE ACTION              #
#####################################################
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
        '0': choose_category,
        '1': manage_favourites,
        'B': quit_app,
        'Q': quit_app,
    }
    choice = view.get_choice(question, answers)
    res.get(str(choice))(choice, db)


#####################################################
#            CHOOSE PRODUCTS IN A CATEGORY          #
#####################################################
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
    res.get(choice, choose_product)(model.CATEGORIES[choice], db)


def choose_product(category, db, warning=''):
    '''
    chose a category
    Arguments:
        category {string}
        db {database}
    '''
    question = 'Which product do you want to substitute?'
    # list of Product
    products = db.get_products(category)
    # list of codes
    products_codes = [product.code for product in products]
    # list of names
    products_names = [product.name for product in products]
    res = {
        'B': choose_category,
        'Q': quit_app,
    }
    choice = view.get_choice(question, products_names, warning)
    # By default, return choose_healthier(Product, db)
    res.get(choice, choose_healthier)(products[choice], db)
    # return view.get_choice(question, list(zip(*products))[1])


def choose_healthier(product, db):
    code = product.code
    category = product.category
    # get product candidtes to be substitutes
    potential_substitutes = db.find_healthier(product)
    # check if there are candidates
    if not potential_substitutes:
        warning = "NO HEALTHIER PRODUCT IN CATEGORY!\n"
        choose_product(product.category, db, warning)
    else:
        question = (
            "Those products are healthier which one do you want to save?")
        # make a choice amongst candidates names
        choice = view.get_choice(
            question, [prod.name for prod in potential_substitutes]
            )
        # res = {
        #     'B': choose_category,
        #     'Q': quit_app,
        # }
        # # By default, return choose_healthier(Product, db)
        # if int(choice) == choice:
        #     res.get(choice)(product.category, db)

        # get the one and then save it.
        substitute = potential_substitutes[choice]

        db.save_favourite(product, substitute)
        print(product)
        print("remplacé par")
        print(substitute)
        choose_action(product.code, db)


#####################################################
#                   MANAGE FAVOURITES               #
#####################################################
def manage_favourites(_, db):
    '''
    chose a category
    Arguments:
        _ unused
        db {database}: database
    '''
    pass


#####################################################
#                      QUIT APP                     #
#####################################################
def quit_app(_, db):
    '''
    Exit app with 2 fake arguments
    '''
    exit


if __name__ == "__main__":
    run()
