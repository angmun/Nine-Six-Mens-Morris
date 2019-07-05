# Author: Lisa Torrey with modifications by Angelica Munyao
# Purpose: Game and player superclasses from which specific games and players inherit and define their behaviors
# Citations: Artifical Intelligence Text Book

from time import sleep, time
# Superclass for games
class Game(object):
    # Check for game equivalence with another
    def __eq__(self, other):
        raise NotImplementedError

    # Hash the game and return its hash code
    def __hash__(self):
        raise NotImplementedError

    # Return the utility of this game if it is over
    # Otherwise, return None
    def utility(self):
        raise NotImplementedError

    # Return a list of possible moves for the game
    def moves(self):
        raise NotImplementedError

    # Return this game's child created by a move
    def child(self, move, player):
        raise NotImplementedError

    # Print the game in the console
    def display(self):
        raise NotImplementedError

    # Estimate the utility of this game
    def evaluate(self, player):
        raise NotImplementedError

    # Play the game
    def play(self, max_player, min_player, interval=1):
        print("Playing game...")
        self.display()
        moves = 0
        game = self
        player, opponent = max_player, min_player

        while game.utility() is None:
            start = time()
            move = player.move(game)
            seconds = time() - start

            if player.maximizes():
                print("Max after", seconds, "seconds.")

            else:
                print("Min after", seconds, "seconds.")

            game = game.child(move, player)
            game.display()
            moves += 1
            sleep(interval)
            player, opponent = opponent, player

        print("Game over with utility", game.utility(), "after", moves, "moves")

# Superclass for players
class Player(object):
    # Return the move this object wants to make
    def move(self, game):
        raise NotImplementedError

    # Return whether this player wants to maximize utility
    def maximizes(self):
        raise NotImplementedError