import numpy as np


def _new(indexes) -> np.array:
    item = np.zeros(16, dtype=np.int8)
    item.put(indexes, 1)
    return item.reshape((4, 4))


ITEMS = {
    "I": np.resize((_new((1, 5, 9, 13)), _new((4, 5, 6, 7))), (4, 4, 4)),
    "J": np.array((_new((2, 6, 9, 10)), _new((4, 5, 6, 10)), _new((1, 2, 5, 9)), _new((0, 4, 5, 6)))),
    "L": np.array((_new((1, 5, 9, 10)), _new((6, 8, 9, 10)), _new((1, 2, 6, 10)), _new((0, 1, 2, 4)))),
    "S": np.resize((_new((5, 6, 8, 9)), _new((1, 5, 6, 10))), (4, 4, 4)),
    "Z": np.resize((_new((4, 5, 9, 10)), _new((2, 5, 6, 9))), (4, 4, 4)),
    "O": np.broadcast_to(_new((5, 6, 9, 10)), (4, 4, 4)),
    "T": np.array((_new((1, 4, 5, 6)), _new((1, 4, 5, 9)), _new((4, 5, 6, 9)), _new((1, 5, 6, 9))))
}
