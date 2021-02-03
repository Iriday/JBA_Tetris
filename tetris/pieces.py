import numpy as np


def _new(indexes) -> np.array:
    item = np.zeros(16, dtype=np.int8)
    item.put(indexes, 1)
    return item.reshape((4, 4))


PIECES = {
    "I": np.resize(((1, 5, 9, 13), (0, 1, 2, 3)), (4, 4)),
    "J": np.array(((2, 6, 9, 10), (0, 1, 2, 6), (1, 2, 5, 9), (1, 5, 6, 7))),
    "L": np.array(((1, 5, 9, 10), (2, 4, 5, 6), (1, 2, 6, 10), (1, 2, 3, 5))),
    "S": np.resize(((1, 2, 4, 5), (1, 5, 6, 10)), (4, 4)),
    "Z": np.resize(((1, 2, 6, 7), (2, 5, 6, 9)), (4, 4)),
    "O": np.broadcast_to((1, 2, 5, 6), (4, 4)),
    "T": np.array(((1, 5, 6, 9), (1, 4, 5, 6), (2, 5, 6, 10), (1, 2, 3, 6)))
}
