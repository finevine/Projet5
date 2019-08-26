'''
The model of the Physical Data model
'''

class Category:
    ''' Class for one of the categories to analyse '''
    def __init__(self, cat_id, cat_name):
        self.id = cat_id
        self.name = cat_name


class Product:
    ''' A product from OpenFood Fact with only interesting attributes'''
    def __init__(self, product):
        self.code = product.get('code', 'not-applicable')
        self.name = product.get('product_name', 'not-applicable')
        self.categories = product.get('categories', 'not-applicable')
        self.nutrition_grade = product.get('nutrition_grade_fr', 'not-applicable')
    

class Favourite(Product):
    ''' A class for saved products '''
    def __init__(self, code_unhealthy, code_healthy):
        super().__init__(code, code_unhealthy, code_healthy)
        # code substitute is the code of the product that it substitute
        self.code_unhealthy = code_unhealthy
        self.code_healthy = code_healthy
