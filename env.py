from enum import Enum 

HOST = 'localhost'
PORT = 54332

games = {
    'boxes': 'Boxes', 
    'chess': 'Chess'}


class MENU_CODE(Enum):
    START = 0
    BOXES = 1
    CHESS = 2

    # game states
    WIN = 3
    LOSE = 4
    DRAW = 5
    DISCONNECTED = 6

menus = dict(enumerate([menu for menu in MENU_CODE]))