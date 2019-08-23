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


class Favourite(Product):
    ''' A class for saved products '''
    def __init__(self, code_unhealthy, code_healthy):
        super().__init__(code, code_unhealthy, code_healthy)
        # code substitute is the code of the product that it substitute
        self.code_unhealthy = code_unhealthy
        self.code_healthy = code_healthy
