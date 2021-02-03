import view as v
import model

piece_name = v.get_piece_name()
m = model.Model(v.get_dimensions())
v.show_game_field(m.game_field)  # show empty field
m.start_round(piece_name)

while True:
    v.show_game_field(m.game_field)
    m.move_piece(v.get_action())
