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

    def start_round(self, piece_name):  # temp
        self.curr_piece_name = piece_name
        self.curr_piece_index = 0
        self.piece_offset = 0
        self.curr_piece_coords = self.adjust_piece_coords(PIECES[self.curr_piece_name][self.curr_piece_index].copy(), self.piece_offset, self.field_width)
        self.place_piece(self.curr_piece_coords, 1)  # place piece at start pos

    def adjust_piece_coords(self, piece_4x4_indexes, piece_offset, field_width):
        len_before = field_width // 2 - 2  # left upper corner (len before piece)
        len_after = field_width - len_before - 4

        with np.nditer(piece_4x4_indexes, op_flags=["readwrite"]) as indexes:
            for i in indexes:
                if i <= 3:
                    i += len_before
                elif i <= 7:
                    i += len_before * 2 + len_after
                elif i <= 11:
                    i += len_before * 3 + len_after * 2
                elif i <= 15:
                    i += len_before * 4 + len_after * 3
                i += piece_offset

        return piece_4x4_indexes

    def place_piece(self, indexes, piece):
        self.game_filed.put(indexes, piece, mode='clip')

    def move_piece(self, action):
        def rotate():
            self.curr_piece_index = (self.curr_piece_index + 1) % 4
            self.curr_piece_coords = self.adjust_piece_coords(PIECES[self.curr_piece_name][self.curr_piece_index].copy(), self.piece_offset, self.field_width)

        def down():
            self.piece_offset += self.field_width
            self.curr_piece_coords += self.field_width

        def left():
            self.piece_offset -= 1
            self.curr_piece_coords[self.curr_piece_coords % self.field_width == 0] += self.field_width
            self.curr_piece_coords -= 1

        def right():
            self.piece_offset += 1
            self.curr_piece_coords += 1
            cols = self.curr_piece_coords % self.field_width == 0
            if np.any(cols):
                self.curr_piece_coords[cols] -= self.field_width

        self.place_piece(self.curr_piece_coords, 0)  # remove previous piece

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

        self.place_piece(self.curr_piece_coords, 1)
