import numpy as np
from enum import Enum, auto
from pieces import PIECES


class Action(Enum):
    ROTATE = auto()
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()


class Model:
    def __init__(self, dimensions):
        self.field_width, self.field_height = dimensions
        self.game_filed = np.zeros((self.field_height, self.field_width), dtype=np.int8)
        self.empty_piece = np.zeros((4, 4))

    def start_round(self, piece_name):  # temp
        self.curr_piece_name = piece_name
        self.curr_piece_index = 0
        self.curr_piece_coords = self.calc_piece_start_pos()
        self.place_piece(self.curr_piece_coords, PIECES[piece_name][self.curr_piece_index])  # place piece at start pos

    def calc_piece_start_pos(self):
        half = self.field_width // 2 - 2
        return np.arange(self.field_width * 4).reshape((4, self.field_width))[:, half:(half + 4)]  # return indexes

    def place_piece(self, indexes, piece):
        self.game_filed.put(indexes, piece, mode='clip')

    def move_piece(self, action):
        def rotate():
            self.curr_piece_index = (self.curr_piece_index + 1) % 4
            self.place_piece(self.curr_piece_coords, PIECES[self.curr_piece_name][self.curr_piece_index])

        def down():
            self.place_piece(self.curr_piece_coords, self.empty_piece)
            self.curr_piece_coords += self.field_width
            self.place_piece(self.curr_piece_coords, PIECES[self.curr_piece_name][self.curr_piece_index])

        if action == Action.ROTATE:
            down()
            rotate()
        elif action == Action.DOWN:
            down()
