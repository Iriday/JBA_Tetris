import numpy as np
from enum import Enum, auto


class Action(Enum):
    ROTATE = auto()
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()


class Model:
    def __init__(self, dimensions):
        self.game_filed = np.zeros(dimensions, dtype=np.int8)

    def perform_action(self, action):
        pass
