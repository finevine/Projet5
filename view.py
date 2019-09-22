'''
Viewer of Foodstitute
'''
from sys import exit
import pdb


def print_title(title):
    ''' print a title centered
    Arguments:
        title {string}
    '''
    # First header of title with '*' char (WIDTH = 64)
    print(
        f"{'*':*^64}",
        f"*{' ': ^62}*",
        sep='\n'
        )
    # split text in lines of 60 char
    title_pieces = split_text(title, 50)
    # print those lines centered
    for title_piece in title_pieces:
        print(f"*{title_piece: ^62}*", sep='\n')
    # print footer of title with '*' char
    print(
        f"*{' ': ^62}*",
        f"{'*':*^64}",
        sep='\n')


def split_text(text, numb):
    ''' function to split a text in *numb* char
    Arguments
        text {string}, numb_of_char {int}
    '''
    res = []
    line = ''

    for word in text.split():
        # check if line + word <= theorical length of line -1 for space
        if len(line) + len(word) <= numb - 1:
            line = line + ' ' + word
        else:
            res.append(line)
            line = word
    res.append(line)
    return res


def start_view():
    print_title(""" WELLCOME!\n
    This is a beta app to find products that can substitute your food.\n
    CAUTION: there might be inaccuracies in nutrition grades.
    """)


def get_choice(question, choices, precision=''):
    ''' Get choice in a list
    Arguments:
        question: {string}
        choices: {list}
    '''
    print(
        '****************************************************************',
        question, sep='\n'
        )
    # list all possibilities
    for choice_num in range(len(choices)):
        print(
            str(choice_num + 1) + ' ' + choices[choice_num],
            sep='\n'
        )
    good_choice = False
    # detect errors in answer
    while not good_choice:
        try:
            choice = input(precision + 'Make your Choice: ').upper()
            # Try if it's an integer
            try:
                int(choice)
                # If not: check if it's Back or Quit
            except ValueError:
                if choice not in ['B', 'Q']:
                    # If not raise error
                    raise ValueError
                else:
                    return choice
            else:
                # Else check if it's in the good range
                if int(choice) not in range(1, len(choices) + 1):
                    raise ValueError
                else:
                    good_choice = True
        except ValueError:
            print(
                'Must be an int in [1,' + str(len(choices)) +
                '] or (B)ack or (Q)uit'
            )
        else:
            # return choice
            return int(choice) - 1


if __name__ == "__main__":
    print('Viewer of Foodstitute')
