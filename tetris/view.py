from items import ITEMS
import numpy as np
import re


def format_item(item):
    return re.sub(r" *[\[\]]", "", np.array2string(item, formatter={"int": lambda v: '-' if (v == 0) else '0'}))


print(format_item(np.zeros((4, 4), dtype=int)), format_item(ITEMS[input()]), sep="\n\n")
