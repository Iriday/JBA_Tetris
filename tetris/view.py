from pieces import PIECES
import numpy as np
import re
import model as m


def format_piece_or_filed(p_or_f):
    return re.sub(r" *[\[\]]", "", np.array2string(p_or_f, formatter={"int": lambda v: '-' if (v == 0) else '0'}))


def get_piece_name():
    while True:
        piece = input("piece: ").strip().upper()
        if piece in PIECES:
            return piece
        else:
            print(f"Error: Unknown piece (choose from: {', '.join(PIECES)}).")


def get_dimensions():
    while True:
        dim_str = input("dimensions: ").strip().split(' ')
        if len(dim_str) == 2 and dim_str[0].isnumeric() and dim_str[1].isnumeric():
            dim_int = tuple(map(int, dim_str))
            if 5 <= dim_int[0] <= 1000 and 5 <= dim_int[1] <= 1000:
                return dim_int

        print("Error: Incorrect dimensions (example: 10 20. min 5x5, max 1000x1000).")


def get_action():
    while True:
        action = input("action: ").strip().upper()
        if action == "EXIT":
            exit()
        elif action in m.Action.__members__:
            return m.Action[action]

        print(f"Error: Unknown action (choose from: {', '.join(m.Action.__members__)}).")


def show_game_filed(filed):
    print(format_piece_or_filed(filed), end="\n\n")
