import view as v
import model
from pieces import PIECES


def run():
    m = model.Model(v.get_dimensions())
    v.show_game_field(m.get_game_field())  # show empty field

    while True:
        action = v.get_action()
        if action in PIECES:
            m.start_round(action)
        elif action == "BREAK":
            m._break()
        else:
            m.move_piece(action)
        v.show_game_field(m.get_game_field())


run()
