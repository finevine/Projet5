'''
Functions used in Foodstitute
'''
from exit_program import exit_program

if __name__ == "__main__":
    print('Functions used in Foodstitute')


def start():
    '''
    Get the first choice of a user
    '''
    # Explain purpose of tool to user
    print('This tools allows you to find product of substitution \namongst data provided by openfoodfacts.com. \nFor now, only 5 categories of products are available. \nSimply make your choice bellow, or input \'Q\' to quit.\n-----')

    # Detect errors in choice input
    choice = '0'
    try:
        while choice not in ['1', '2']:
            choice = input('(1) Find a substitute\n(2) Manage my food\n\nChoice: ')
            if choice == 'Q':
                exit_program()
            elif choice not in ['1', '2']:
                print('Choice must be 1 OR 2.')
            print('-----')
    except ValueError:
        print('Choice must be 1 OR 2.')
    else:
        return int(choice)


def choose_category(categories):
    '''

    '''
    prompt = 'Choose a category of products:\n'
    for category in categories:
        prompt = prompt + '(' + str(categories.index(category)) + ') ' + category.replace('-', ' ') + '\n'
    choice = input(prompt + '\nChoice: ')
    print('-----')
    return int(choice)


def manage_personnal_food():
    pass


def init_prod_db():
    '''
    Initialize the product database
    '''
