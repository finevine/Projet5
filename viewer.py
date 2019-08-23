'''
Viewer of Foodstitute
'''
from sys import exit
TERMINAL_WIDTH = 50


def print_title(title):
    ''' print a title '''
    print(
        f"{'*':*^54}",
        f"*{' ': ^52}*",
        sep='\n'
        )
    if len(title) <= 50 + 4:
        print(
            f"*{title: ^52}*",
            sep='\n'
        )
    else:
        pieces_title = []
        while title:
            pieces_title.append(title[:49])
            title = title[49:]
        for title_piece in pieces_title:
            print(f"*{title_piece: ^52}*", sep='\n')
    print(
        f"*{' ': ^52}*",
        f"{'*':*^54}",
        sep='\n')


if __name__ == "__main__":
    print_title("JE m'appelle Vincent et je suis super content de pouvoir faire ça.")
    print('Viewer of Foodstitute')