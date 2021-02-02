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

        def down():
            self.curr_piece_coords += self.field_width

        def left():
            cols = self.curr_piece_coords[0:1, 0:4].flatten() % self.field_width == 0
            if np.any(cols):
                self.curr_piece_coords[:, cols] += self.field_width
            self.curr_piece_coords -= 1

        def right():
            self.curr_piece_coords += 1
            cols = self.curr_piece_coords[0:1, 0:4].flatten() % self.field_width == 0
            if np.any(cols):
                self.curr_piece_coords[:, cols] -= self.field_width

        self.place_piece(self.curr_piece_coords, self.empty_piece)  # remove previous piece

        if action == Action.ROTATE:
            down()
            rotate()
        elif action == Action.DOWN:
            down()
        elif action == Action.LEFT:
            down()
            left()
        elif action == Action.RIGHT:
            down()
            right()

        self.place_piece(self.curr_piece_coords, PIECES[self.curr_piece_name][self.curr_piece_index])
