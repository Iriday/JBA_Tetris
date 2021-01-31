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

    def calc_piece_start_pos(self):
        half = self.field_width // 2 - 2
        return np.arange(self.field_width * 4).reshape((4, self.field_width))[:, half:(half + 4)]  # return indexes

    def place_piece(self, indexes, piece):
        self.game_filed.put(indexes, piece, mode='clip')

    def perform_action(self, action):
        pass
