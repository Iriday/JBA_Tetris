import numpy as np
from enum import Enum, auto
from pieces import PIECES
import random


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
    __PIECE_NAMES = tuple(PIECES.keys())

    def __init__(self, dimensions):
        self.field_width = dimensions[0] + 2  # +2 walls
        self.field_height = dimensions[1] + 1  # + floor
        self.game_field = Model.__create_game_field(self.field_width, self.field_height)
        self.__piece_frozen = True
        self.rand = random.Random()

    def __start_round(self, piece_name, piece_state):  # temp
        self.__piece_name = piece_name
        self.__piece_state = piece_state
        self.__piece_offset = 0
        self.__adjust_indexes = lambda: Model.__adjust_piece_indexes(
            PIECES[self.__piece_name][self.__piece_state].copy(),
            self.__piece_offset, self.field_width)
        self.__piece_indexes = self.__adjust_indexes()
        self.__piece_frozen = False

        game_over = self.__game_over()

        Model.__draw_piece(self.game_field, self.__piece_indexes, 1)  # place piece at start pos

        return not game_over

    def start_round(self):
        return self.__start_round(self.rand.choice(Model.__PIECE_NAMES), self.rand.randint(0, 3))  # chose random piece

    def move_piece(self, action):
        if self.__piece_frozen:
            return

        def rotate():
            self.__piece_state = (self.__piece_state + 1) % 4
            self.__piece_indexes = self.__adjust_indexes()
            if Model.__collision_detected(self.game_field, self.__piece_indexes):  # revert piece move
                self.__piece_state = (self.__piece_state + 3) % 4
                self.__piece_indexes = self.__adjust_indexes()

        def down():
            self.__piece_indexes += self.field_width
            if Model.__collision_detected(self.game_field, self.__piece_indexes):  # revert piece move
                self.__piece_indexes -= self.field_width
                return
            self.__piece_offset += self.field_width

        def left():
            self.__piece_indexes -= 1
            if Model.__collision_detected(self.game_field, self.__piece_indexes):  # revert piece move
                self.__piece_indexes += 1
                return
            self.__piece_offset -= 1

        def right():
            self.__piece_indexes += 1
            if Model.__collision_detected(self.game_field, self.__piece_indexes):  # revert piece move
                self.__piece_indexes -= 1
                return
            self.__piece_offset += 1

        Model.__draw_piece(self.game_field, self.__piece_indexes, 0)  # remove previous piece

        if action == Action.ROTATE:
            rotate()
        elif action == Action.LEFT:
            left()
        elif action == Action.RIGHT:
            right()
        down()  # also if action == Action.DOWN:

        # froze piece if it hit the floor
        if Model.__collision_detected(self.game_field, self.__piece_indexes + self.field_width):
            self.__piece_frozen = True

        Model.__draw_piece(self.game_field, self.__piece_indexes, 1)

        if self.round_ended():
            self.__break()  # clear row(s) if filled

    def get_game_field(self):
        return self.game_field[0:self.field_height - 1, 1:self.field_width - 1]

    def round_ended(self):
        return self.__piece_frozen

    def __break(self):
        i = len(self.game_field) - 2
        while i >= 0:
            if np.all(self.game_field[i]):
                self.game_field[1:i + 1] = self.game_field[0:i]
                self.game_field.put(np.arange(1, self.field_width - 1), 0)
                continue
            i -= 1

    def __game_over(self):
        return self.__collision_detected(self.game_field[0:4, :], self.__piece_indexes)

    # Static methods ------------------
    @staticmethod
    def __create_game_field(width, height):
        field = np.zeros((height, width), dtype=np.int8)
        field[:, [0, width - 1]] += 1
        field[height - 1] += 1
        return field

    @staticmethod
    def __adjust_piece_indexes(piece_4x4_indexes, piece_offset, field_width):
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
    def __collision_detected(game_field, piece):
        return len(np.intersect1d(np.flatnonzero(game_field), piece)) > 0

    @staticmethod
    def __draw_piece(game_field, indexes, piece):
        game_field.put(indexes, piece, mode='clip')
