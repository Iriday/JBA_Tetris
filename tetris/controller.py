import view as v
import model
from pieces import PIECES


def run():
    m = model.Model(v.get_dimensions())
    v.show_game_field(m.get_game_field())  # show empty field

    while True:
        action = v.get_action()
        if action == "EXIT":
            exit()
        elif action in PIECES:
            started = m.start_round(action)
            if not started:
                v.show_game_over()
                exit()
        elif action == "BREAK":
            m.break_()
        else:
            m.move_piece(action)
        v.show_game_field(m.get_game_field())


run()
