'''
Controller of Foodstitute
'''
import settings
import model
import view


def compare_products(code_product, db):
    ''' compare 2 products of the database'''
    # trier par catégories dans les 10 premiers méthode de produits
    pass
    # return product


def start():
    view.start_view()


def run():
    step = 0
    question = 'Which category of product you want to use?'
    choice_list = model.CATEGORIES
    while step >= 0:
        choice, step = view.get_choice(question, choice_list, step)
        print(choice, step)


if __name__ == "__main__":
    view.start_view()
    run()
