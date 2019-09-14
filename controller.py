'''
Controller of Foodstitute
'''
import settings
import model
import view


def main():
    db = DataBase()
    db.create_tables()
    db.feed_database(Category('nuts'))
    # breakpoint()
    # print(Category('nuts').get_api_products())
    db.connection.commit()
    db.connection.close()
    

def compare_products(code_product):
    ''' compare 2 products of the database'''
    # trier par catégories dans les 10 premiers méthode de produits
    pass
    # return product


def start():
    view.start_view()

if __name__ == "__main__":
    print('Controller used in Foodstitute')
    # test_api('candies')
    view.get_choice(model.CATEGORIES)
