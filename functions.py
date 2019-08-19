'''
Functions used in Foodstitute
'''
if __name__ == "__main__":
    print('Functions used in Foodstitute')


def start():
    '''
    Get the first choice of a user
    '''
    choice = ''
    try:
        while choice not in [1, 2]:
            choice = int(input('- Find a substitute (1)\n- Manage my food (2)\nChoice:'))
            if choice not in [1, 2]:
                print('Choice must be 1 OR 2.')
    except ValueError:
        print('Choice must be 1 OR 2.')
    else:
        return choice
