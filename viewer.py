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
    ''' function to split a text in *numb* char '''
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

if __name__ == "__main__":
    print('Viewer of Foodstitute')
    print_title("et dans le viewer j'ai mis des fonctions (tout comme dans le controller) mais je comprends qu'il faut que j'ajoute une classe db avec initialize, add, compare. Je pensais pouvoir mettre ça dans mon controllerje pense qu'il faut que je change de mentor. Elle m'a dit que mon model.py était parfait.")
