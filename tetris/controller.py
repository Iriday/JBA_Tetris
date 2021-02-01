import view as v
import model

piece_name = v.get_piece_name()
m = model.Model(v.get_dimensions())
v.show_game_filed(m.game_filed)  # show empty field
m.start_round(piece_name)

while True:
    v.show_game_filed(m.game_filed)
    m.perform_action(v.get_action())
