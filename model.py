'''
The model of the Physical Data model
'''

class Category:
    ''' class for one of the categories to analyse '''
    def __init__(self, cat_id, cat_name):
        self.id = cat_id
        self.name = cat_name


class Product:
    ''' A product from OpenFood Fact with only interesting attributes'''
    def __init__(self, code, product_name, categories, nutrition_grade):
        self.code = code
        self.product_name = product_name
        self.categories = categories
        self.nutrition_grade = nutrition_grade


class Substitute(Product):
    ''' A class for a saved substitute '''
    def __init__(self, code, product_name, categories, nutrition_grade, code_substitute):
        super().__init__(code, product_name, categories, nutrition_grade)
        # code substitute is the code of the product that it substitute
        self.code_substitute = code_substitute


class Favourite(Product):
    ''' A class for saved products '''
    def __init__(self, code, product_name, categories, nutrition_grade):
        super().__init__(code, product_name, categories, nutrition_grade, code_favourite)
        # code substitute is the code of the product that it substitute
        self.code_favourite = code_favourite