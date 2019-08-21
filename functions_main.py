'''
Functions used in Foodstitute
'''
from sys import exit
if __name__ == "__main__":
    print('Functions used in Foodstitute')


def read_categories(path):
    data = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                data.append(line)
    return data

CATEGORIES = read_categories('./src/categories.txt')

def start():
    '''
    Get the first choice of a user
    '''
    # Explain purpose of tool to user
    print('***********************************************************',
          '*                      FOODSTITUTE                        *',
          '*          CAUTION : this program is in beta              *',
          '*            and products are not accurate.               *',
          '***********************************************************',
          'Make your choice bellow, or \'Q\' to quit :\n-----',
          sep='\n')

    # Detect errors in choice input
    choice = input('(1) Find a substitute\n(2) Manage my food\n\nChoice: ').upper()

    while choice not in ['1', '2', 'B', 'Q']:
        print('Choice must be 1 OR 2.',
              '-----',
              sep='\n')
        choice = input('(1) Find a substitute\n(2) Manage my food\n\nChoice: ').upper()
    print('-----')

    return choice


def run(choice):
    '''
    Main run funtion
    '''
    if choice == '1':
        res = substitute(CATEGORIES)
    elif choice == '2':
        res = manage_personnal_food()
    elif choice == 'Q':
        exit_program()
    else:
        res = start()

    return res


def substitute(categories):
    '''
    Substitute and eventually save substituted product
    '''
    # Find a category of product
    category = find_category(categories)
    # Find a product to substitute
    product = find_product(category)
    # Save (or not) a product
    save(product)
    # Back to first menu
    return start()


def find_category(categories):
    '''
    Choose a category of product user want to substitude
    '''
    prompt = 'Choose a category of products:\n'
    possible_choices = ['Q', 'B']

    # List all categories
    for category in categories:
        prompt = prompt + '(' + str(categories.index(category)) + ') '\
                 + category.replace('-', ' ') + '\n'
        possible_choices.append(str(categories.index(category)))
    choice = input(prompt + '\nChoice: ').upper()

    while choice not in possible_choices:
        print('Choice must be a (#) category, (B)ack or (Q)uit.')
        print('-----')
        choice = input(prompt + '\nChoice: ').upper()
    print('-----')

    # Return choosen category
    return choice

def find_product(category):
    '''
    Find a product in a category
    '''
    return True

def save(product):
    '''
    Save a given product to personnal database
    '''
    pass

def manage_personnal_food():
    '''
    Manage personnal food in the database
    '''
    return 'B'


def connect_client():
    pass

def exit_program():
    '''
    Exit the program
    '''
    print('You have exited the tool. Thanks!\n')
    exit()
