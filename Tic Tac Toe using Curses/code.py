import curses
import curses.ascii
import numpy as np

X = ord('x'), ord('X')
O = ord('o'), ord('O')

up = ord('w'), ord('W'), curses.KEY_UP
down = ord('s'), ord('S'), curses.KEY_DOWN
right = ord('d'), ord('D'), curses.KEY_RIGHT
left = ord('a'), ord('A'), curses.KEY_LEFT
reset = ord('r'), ord('R')
exit = ord('q'), ord('Q')
button = ord('b'), ord('B')

plansza = (
    '{}|{}|{}\n'
    '-+-+-\n'
    '{}|{}|{}\n'
    '-+-+-\n'
    '{}|{}|{}\n'
)

def new_game():
    return np.array([[None] * 3] * 3)

def winner(game):
    for player in chr(X[-1]), chr(O[-1]):
        if any((
            # check diagonals
            set(game.diagonal()) == {player},
            set(np.fliplr(game).diagonal()) == {player},
            # check rows
            {player} in map(set, game),
            # check columns
            {player} in map(set, game.T)
        )):
            return player

def cell(y, x):
    return y // 2, x // 2

def key(value):
    key, *_ = value
    return chr(key)

def run(game):
    gracz = 'O'
    window = curses.initscr()
    window.clear()
    window.keypad(True)
    curses.noecho()
    try:
        y, x = 0, 0
        value = None

        while not value in exit:
            board = plansza.format(*((v or ' ') for v in game.flatten()))
            window.addstr(0, 0, board)

            ruch = f'{gracz} Player turn'
            window.addstr(6, 0, ruch)

            value = window.getch(y, x)

            if value in up:
                y = max(0, y-2)
            elif value in down:
                y = min(5, y+2)
            elif value in right:
                x = min(5, x+2)
            elif value in left:
                x = max(0, x-2)
            elif value in button:
                if gracz == 'O' and game[cell(y, x)] != chr(O[-1]) and game[cell(y, x)] != chr(X[-1]):
                    game[cell(y, x)] = chr(O[-1])
                    gracz = 'X'
                elif gracz == 'X' and game[cell(y, x)] != chr(O[-1]) and game[cell(y, x)] != chr(X[-1]):
                    game[cell(y, x)] = chr(X[-1])
                    gracz = 'O'
            elif value in reset:
                game = new_game()
            else:
                curses.flash()
            player = winner(game)

            if player:
                window.addstr(8, 0, f'{player} wins!')
            elif np.all(game != None):
                window.addstr(8, 0, "draw! ")
            else:
                window.addstr(8, 0, ' ' * 10)

    finally:
        curses.endwin()

if __name__ == '__main__':
    run(new_game())
