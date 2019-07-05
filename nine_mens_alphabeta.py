# Test of the alpha-beta mini-max agents with depth limiting on Nine Men's Morris board

from alphabeta9 import MaxPlayer, MinPlayer
from nine_men_morris import NineMensMorris
max_player = MaxPlayer()
min_player = MinPlayer()

max_player.assume(min_player)
min_player.assume(max_player)

game = NineMensMorris()
game.play(max_player, min_player)
