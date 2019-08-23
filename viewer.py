'''
Viewer of Foodstitute
'''
from sys import exit


def print_title(title):
    ''' print a title '''
    # First header of title with '*' char (WIDTH = 64)
    print(
        f"{'*':*^64}",
        f"*{' ': ^62}*",
        sep='\n'
        )
    # check title length
    if len(title) <= 60:
        print(
            f"*{title: ^62}*",
            sep='\n'
        )
    else:
        # split title in pieces apart
        pieces_title = []
        while title:
            pieces_title.append(title[:59])
            title = title[59:]
        # print the pieces
        for title_piece in pieces_title:
            print(f"*{title_piece: ^62}*", sep='\n')
    # print footer of title with '*' char
    print(
        f"*{' ': ^62}*",
        f"{'*':*^64}",
        sep='\n')


if __name__ == "__main__":
    print_title("JE m'appelle Vincent et je suis super content.")
    print('Viewer of Foodstitute')