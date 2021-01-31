import view as v
import model
from pieces import PIECES

piece_name = v.get_piece_name()
m = model.Model(v.get_dimensions())
v.show_game_filed(m.game_filed)  # show empty field
m.place_piece(m.calc_piece_start_pos(), PIECES[piece_name][0])  # place piece at start pos

while True:
    v.show_game_filed(m.game_filed)
    m.perform_action(v.get_action())
