'''
Controller of Foodstitute
'''
import settings
import model
import view
import argparse
import pdb
from random import randint
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
    res.get(choice)(_, db)


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
    question = 'Which category of product do you want to use?'
    answers = model.CATEGORIES
    res = {
        'B': choose_action,
        'Q': quit_app,
    }
    choice = view.get_choice(question, answers)
    # Default is choose_product, else choose_action or quit_app
    if choice.isdigit():
        next_parameter = answers[int(choice)]
    else:
        next_parameter = choice
    # call chosen function with next_parameter
    res.get(choice, choose_product)(next_parameter, db)


def choose_product(category, db, warning=''):
    '''
    chose a product in a category
    Arguments:
        category {string}
        db {database}
    '''
    question = 'Which product do you want to substitute?'
    res = {
        'B': choose_category,
        'Q': quit_app,
    }
    # list of Product
    products = db.get_products(category)
    # list of codes
    products_codes = [product.code for product in products]
    # list of names
    products_names = [
        prod.name + ' (' + prod.nutrition_grade.upper() + ')'
        for prod in products
        ]
    choice = view.get_choice(question, products_names, warning)
    if choice.isdigit():
        next_parameter = products[int(choice)]
    else:
        next_parameter = choice
    # By default, return random_healthier
    res.get(choice, random_healthier)(next_parameter, db)


def random_healthier(product, db):
    '''
    Pick a random healthier product in a category
    Arguments:
        product {Product}
        db {Database}
    '''
    def OK_for_substitute(substitute_list, database, answer='1'):
        question = "Do you want to save it?"
        answers = ['Yes', 'No']
        res = {
            '0': save_it,
            'B': choose_product,
            'Q': quit_app
        }
        while answer == '1':
            print('This product is healthier')
            # pick a random substitute
            substitute = substitute_list[
                randint(0, len(substitute_list) - 1)
                ]
            print(substitute)
            answer = view.get_choice(question, answers)
        if answer == 'B':
            next_parameter = substitute.category
        else:
            next_parameter = substitute

        res.get(answer)(next_parameter, database)

    def save_it(substitute, database, prod=product):
        database.save_favourite(prod, substitute)
        print(substitute)
        print("****REPLACES:")
        print(prod)
        choose_action(prod.code, database)

    code = product.code
    category = product.category
    # get product candidtes to be substitutes
    potential_substitutes = db.find_healthier(product)
    # check if there are candidates
    if not potential_substitutes:
        warning = "NO HEALTHIER PRODUCT IN CATEGORY!\n"
        choose_product(product.category, db, warning)
    else:
        OK_for_substitute(potential_substitutes, db)


# def choose_healthier(product, db):
#     '''
#     Choose a healthier product in a category
#     Arguments:
#         product {Product}
#         db {Database}
#     '''
#     # Note this function is not used.
#     # The program will now pick a random healthier product
#     code = product.code
#     category = product.category
#     # get product candidtes to be substitutes
#     potential_substitutes = db.find_healthier(product)
#     # check if there are candidates
#     if not potential_substitutes:
#         warning = "NO HEALTHIER PRODUCT IN CATEGORY!\n"
#         choose_product(product.category, db, warning)
#     else:
#         question = (
#             "Those products are healthier. Which one do you want to save?")
#         # make a choice amongst candidates names
#         styled_list = [
#             prod.name + ' (' + prod.nutrition_grade.upper() + ')'
#             for prod in potential_substitutes
#             ]
#         choice = view.get_choice(
#             question, styled_list
#             )
#         # get the one and then save it.
#         substitute = potential_substitutes[int(choice)]

#         db.save_favourite(product, substitute)
#         print(substitute)
#         print("****REPLACE:")
#         print(product)
#         choose_action(product.code, db)


#####################################################
#                   MANAGE FAVOURITES               #
#####################################################
def manage_favourites(_, db):
    '''
    Manage favourites
    Arguments:
        _ unused
        db {database}: database
    '''
    question = 'Which favourite to delete?\n'
    res = {
        'B': choose_action,
        'Q': quit_app,
    }
    # list of favourites
    favourites = db.list_favourites()
    # build the fav view of all favourites
    fav_view = []
    for fav in favourites:
        product = fav[0]
        substitute = fav[1]
        fav_view.append(
            product.category + ': ' +
            substitute.name + ' (' + substitute.purchase + ')\n ' + ' REPLACE: ' + product.name
            )

    choice = view.get_choice(question, fav_view, 'Yes, ' + question)
    if choice.isdigit():
        next_parameter = favourites[int(choice)]
    else:
        next_parameter = choice
    # By default, return confirm
    res.get(choice, confirm_delete_favourite)(next_parameter, db)


def confirm_delete_favourite(favourite, db):
    '''
    Confirm deletion a favourite in db
    Arguments:
        favourite {(Product, Product)}
        db {Database}
    '''
    question = 'Are you sure you want to delete this favourite?'
    res = {
        '1': manage_favourites,
        'B': manage_favourites,
        'Q': quit_app,
    }
    choice = view.get_choice(question, ['Yes', 'No'], '')
    # breakpoint()
    if choice == '0':
        db.delete_favourite(favourite)
        choose_action(favourite, db)
    else:
        res.get(choice)(favourite, db)


#####################################################
#                      QUIT APP                     #
#####################################################
def quit_app(_, db):
    '''
    Exit app with 1 fake arguments
    '''
    connection = db.connection
    # Commit changes
    db.connection.commit()
    # Finally close connection
    connection.close()
    exit


if __name__ == "__main__":
    run()
