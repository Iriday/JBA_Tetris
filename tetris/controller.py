import view as v
import model

piece = v.get_piece_name()
m = model.Model(v.get_dimensions())

while True:
    v.show_game_filed(m.game_filed)
    m.perform_action(v.get_action())
