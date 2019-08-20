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
    print('This tools allows you to find product of substitution \n\
          amongst data provided by openfoodfacts.com. \n\
          For now, only 5 categories of products are available. \n\
          Simply make your choice bellow, or input \'Q\' to quit.\n-----')

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
    Choose a category of product user want to substitude
    '''
    prompt = 'Choose a category of products:\n'

    # List all categories
    for category in categories:
        prompt = prompt + '(' + str(categories.index(category)) + ') '\
                 + category.replace('-', ' ') + '\n'
    choice = input(prompt + '\nChoice: ')
    print('-----')

    # Return choosen category
    return int(choice)


def manage_personnal_food():
    pass


def connect_client():
    pass
