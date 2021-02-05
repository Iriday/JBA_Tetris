import view as v
import model


def run():
    m = model.Model(v.get_dimensions())

    while True:
        if m.round_ended():
            started = m.start_round()
            if not started:
                v.show_game_over()
                exit()
            v.show_game_field(m.get_game_field())  # show piece at start pos

        action = v.get_action()
        if action == "EXIT":
            exit()

        m.move_piece(action)
        v.show_game_field(m.get_game_field())


run()
