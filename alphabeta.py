#Citations: Artifical Intelligence Text Book

from project1.framework import Player
from math import inf

class MiniMaxPlayer(Player):
    # Initialize the player without an opponent initially
    def __init__(self):
        self.opponent = None

    # Set the player's opponent
    def assume(self, opponent):
        self.opponent = opponent

    # Return whether the player maximizes or not
    def maximizes(self):
        raise NotImplementedError

    # Return the move selected by the player
    def move(self, game):
        return self.value(game)[1]

    # Return the best value of the game for the player
    def value(self, game):
        raise NotImplementedError


class MaxPlayer(MiniMaxPlayer):

    def maximizes(self):
        return True

    # Return the best value and move for MAX in this game
    def value(self, game, alpha=-inf, beta=+inf, depth=0):
        # Is the game over?
        utility = game.utility()

        # Check if we have reached the maximum search depth as per our definition
        if utility is None and depth >= 5:
            # Use an evaluation function to estimate the outcome of a game
            return game.evaluate(), None

        # If the utility is available, return it
        if utility is not None:
            return utility, None

        # Which move leads to the best outcome?
        best_value = -inf
        best_move = None

        for move in game.moves():
            child = game.child(move, self)
            value = self.opponent.value(child, alpha, beta, depth + 1)[0]

            # Maximizing
            if best_move is None or value > best_value:
                best_value = value
                best_move = move

            # Pruning
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break

        return best_value, best_move


class MinPlayer(MiniMaxPlayer):

    def maximizes(self):
        return False

    # Return the best value and move for MIN in this game
    def value(self, game, alpha=-inf, beta=+inf, depth=0):
        # Is the game over?
        utility = game.utility()

        # Check if we have reached the maximum search depth as per our definition
        if utility is None and depth >= 5:
            # Use an evaluation function to estimate the outcome of a game
            return game.evaluate(), None

        # If the utility is available, return it
        if utility is not None:
            return utility, None

        # Which move leads to the best outcome?
        best_value = +inf
        best_move = None

        for move in game.moves():
            child = game.child(move, self)
            value = self.opponent.value(child, alpha, beta, depth + 1)[0]

            # Minimizing
            if best_move is None or value < best_value:
                best_value = value
                best_move = move

            # Pruning
            beta = min(beta, best_value)
            if beta <= alpha:
                break

        return best_value, best_move
