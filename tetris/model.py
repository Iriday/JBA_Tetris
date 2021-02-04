import numpy as np
from enum import Enum, auto
from pieces import PIECES


class Action(Enum):
    ROTATE = auto()
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()
    W = ROTATE
    A = LEFT
    D = RIGHT
    S = DOWN


class Model:
    def __init__(self, dimensions):
        self.field_width = dimensions[0] + 2  # +2 walls
        self.field_height = dimensions[1] + 1  # + floor
        self.game_field = Model._create_game_field(self.field_width, self.field_height)

    def start_round(self, piece_name):  # temp
        self.piece_name = piece_name
        self.piece_state = 0
        self.piece_offset = 0
        self.__adjust_indexes = lambda: Model._adjust_piece_indexes(PIECES[self.piece_name][self.piece_state].copy(),
                                                                    self.piece_offset, self.field_width)
        self.piece_indexes = self.__adjust_indexes()
        self.piece_frozen = False
        Model._draw_piece(self.game_field, self.piece_indexes, 1)  # place piece at start pos

    def move_piece(self, action):
        if self.piece_frozen:
            return

        def rotate():
            self.piece_state = (self.piece_state + 1) % 4
            self.piece_indexes = self.__adjust_indexes()
            if Model._collision_detected(self.game_field, self.piece_indexes):  # revert piece move
                self.piece_state = (self.piece_state + 3) % 4
                self.piece_indexes = self.__adjust_indexes()

        def down():
            self.piece_indexes += self.field_width
            if Model._collision_detected(self.game_field, self.piece_indexes):  # revert piece move
                self.piece_indexes -= self.field_width
                return
            self.piece_offset += self.field_width

        def left():
            self.piece_indexes -= 1
            if Model._collision_detected(self.game_field, self.piece_indexes):  # revert piece move
                self.piece_indexes += 1
                return
            self.piece_offset -= 1

        def right():
            self.piece_indexes += 1
            if Model._collision_detected(self.game_field, self.piece_indexes):  # revert piece move
                self.piece_indexes -= 1
                return
            self.piece_offset += 1

        Model._draw_piece(self.game_field, self.piece_indexes, 0)  # remove previous piece

        if action == Action.ROTATE:
            rotate()
        elif action == Action.LEFT:
            left()
        elif action == Action.RIGHT:
            right()
        down()  # also if action == Action.DOWN:

        # froze piece if it hit the floor
        if Model._collision_detected(self.game_field, self.piece_indexes + self.field_width):
            self.piece_frozen = True

        Model._draw_piece(self.game_field, self.piece_indexes, 1)

    def get_game_field(self):
        return self.game_field[0:self.field_height - 1, 1:self.field_width - 1]

    # Static methods ------------------
    @staticmethod
    def _create_game_field(width, height):
        field = np.zeros((height, width), dtype=np.int8)
        field[:, [0, width - 1]] += 1
        field[height - 1] += 1
        return field

    @staticmethod
    def _adjust_piece_indexes(piece_4x4_indexes, piece_offset, field_width):
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

    @staticmethod
    def _collision_detected(game_field, piece):
        return len(np.intersect1d(np.flatnonzero(game_field), piece)) > 0

    @staticmethod
    def _draw_piece(game_field, indexes, piece):
        game_field.put(indexes, piece, mode='clip')
