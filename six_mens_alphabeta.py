# Test of the alpha-beta mini-max agents with depth limiting on Six Men's Morris board

from alphabeta6 import MaxPlayer, MinPlayer
from six_men_morris import SixMensMorris
max_player = MaxPlayer()
min_player = MinPlayer()

max_player.assume(min_player)
min_player.assume(max_player)

game = SixMensMorris()
game.play(max_player, min_player)
