# Author: Angelica Munyao
# Title: Six Men's Morris Game Project
# Citations: Nine Men's Morris Game Description: https://en.wikipedia.org/wiki/Nine_men%27s_morris#Six_men's_morris
#            Python pass-by-reference or pass-by-value: https://jeffknupp.com/blog/2012/11/13/is-python-callbyvalue-or-callbyreference-neither/
#            Nine Men's Morris: Evaluation Functions paper by Simona-Alexandra Petcu and Stefan Holban, 2008

from project1.framework import Game
from copy import deepcopy

# Unplayed board configuration
INITIAL_BOARD = [[' ' for x in range(8)] for y in range(2)]


class SixMensMorris(Game):
    # Create a game object:
    # The board starts empty with no players yet and each player having 6 pieces to use with 0 on the board
    def __init__(self, board=INITIAL_BOARD, last_player=None, max_pieces=6, min_pieces=6, max_loc=set(), min_loc=set()):
        self.board = board
        self.last_player = last_player
        self.max_pieces = max_pieces
        self.min_pieces = min_pieces

        # Track the locations of player pieces and spaces available on the board
        self.max_loc = max_loc
        self.min_loc = min_loc
        self.spaces = {(x, y) for x in range(2) for y in range(8)} - self.max_loc - self.min_loc

    # Check for game equivalence with another:
    # This means the same number of pieces for each player and the same board configuration
    def __eq__(self, other):
        return self.board == other.board and self.max_pieces == other.max_pieces and self.min_pieces == other.min_pieces

    # Hash the game and return its hash code
    def __hash__(self):
        return hash(str(self.board) + str(self.max_pieces) + str(self.min_pieces))

    # Return the utility of this game if it is over: Max winning is 1, Min winning is -1
    # Otherwise, return None
    def utility(self):
        # We are at the beginning of the game
        if self.last_player is None:
            return None

        # The game is over if one of the players only has two pieces left on the board
        if (not self.last_player.maximizes()) and self.max_pieces == 0 and len(self.max_loc) == 2:
            return -1

        if self.last_player.maximizes() and self.min_pieces == 0 and len(self.min_loc) == 2:
            return 1

        # The game is also over if one of the players have no more moves to make
        if not self.moves():
            if self.last_player.maximizes():
                return 1

            else:
                return -1

    # Helper functions to check how close a mill would be for a player
    # Check for already existing mills
    def has_mill(self, locations):
        mill_count = 0

        # Keep track of mills that have already been determined
        counted = set()

        for loc in locations:
            x, y = loc

            # The piece is located at the middle of a line on the board
            if y % 2 == 1:
                # Check if the necessary adjacent pieces are also available
                potential_mill = {(x, (y - 1) % 8), (x, y), (x, (y + 1) % 8)}

                if potential_mill.issubset(locations) and not \
                        potential_mill.issubset(counted):
                    # Add the mill to our set of counted mills
                    counted |= potential_mill
                    mill_count += 1

            # The piece is located at the corner of a square on the grid
            else:
                # Check if the necessary adjacent pieces are also available
                potential_mill1 = {(x, (y - 1) % 8), (x, (y - 2) % 8), (x, y)}
                potential_mill2 = {(x, y), (x, (y + 1) % 8), (x, (y + 2) % 8)}

                # Before the piece location
                if potential_mill1.issubset(locations) and not potential_mill1.issubset(counted):
                    # Add the mill to our set of counted mills
                    counted |= potential_mill1
                    mill_count += 1

                # After the piece location
                if potential_mill2.issubset(locations) and not potential_mill2.issubset(counted):
                    # Add the mill to our set of counted mills
                    counted |= potential_mill2
                    mill_count += 1

        return mill_count

    # Check how many pairs only require a piece to become a mill
    # If in phase 2 of the game, we check if a move is available to complete the potential mill
    def one_to_mill(self, locations, phase):
        mill_count = 0

        # Keep track of potential mills that have already been determined
        counted = set()

        for loc in locations:
            x, y = loc

            # The piece is located at the middle of a line on the board
            if y % 2 == 1:
                # Check for an adjacent left piece and a right space
                if (x, (y - 1) % 8) in locations and (x, (y + 1) % 8) in self.spaces and not \
                        {(x, (y - 1) % 8), (x, y)}.issubset(counted):
                    if phase != 2 or (phase == 2 and (x, (y + 2) % 8) in locations):
                        # Add the accounted for pair to the set of counted mill potentials
                        counted |= {(x, (y - 1) % 8), (x, y)}
                        mill_count += 1

                # Check for an adjacent right piece and a left space
                if (x, (y + 1) % 8) in locations and (x, (y - 1) % 8) in self.spaces and not \
                        {(x, (y + 1) % 8), (x, y)}.issubset(counted):
                    if phase != 2 or (phase == 2 and (x, (y - 2) % 8) in locations):
                        # Add the accounted for pair to the set of counted mill potentials
                        counted |= {(x, (y + 1) % 8), (x, y)}
                        mill_count += 1

            # The piece is located at the corner of a square on the grid
            else:
                # Check for an adjacent left piece and a further left space
                if (x, (y - 1) % 8) in locations and (x, (y - 2) % 8) in self.spaces and not \
                        {(x, (y - 1) % 8), (x, y)}.issubset(counted):
                    if phase != 2 or (phase == 2 and (x, (y - 3) % 8) in locations):
                        # Add the accounted for pair to the set of counted mill potentials
                        counted |= {(x, (y - 1) % 8), (x, y)}
                        mill_count += 1

                # Check for an adjacent right piece and a further right space
                if (x, (y + 1) % 8) in locations and (x, (y + 2) % 8) in self.spaces and not \
                        {(x, (y + 1) % 8), (x, y)}.issubset(counted):
                    if phase != 2 or (phase == 2 and (x, (y + 3) % 8) in locations):
                        # Add the accounted for pair to the set of counted mill potentials
                        counted |= {(x, (y + 1) % 8), (x, y)}
                        mill_count += 1

                # Check for a corner piece on the same line with a center space
                if (x, (y - 2) % 8) in locations and (x, (y - 1) % 8) in self.spaces and not \
                        {(x, (y - 2) % 8), (x, y)}.issubset(counted):
                    if phase != 2 or (phase == 2 and ((x + 1) % 2, (y - 1) % 8) in locations):
                        # Add the accounted for pair to the set of counted mill potentials
                        counted |= {(x, (y - 2) % 8), (x, y)}
                        mill_count += 1

                if (x, (y + 2) % 8) in locations and (x, (y + 1) % 8) in self.spaces and not \
                        {(x, (y + 2) % 8), (x, y)}.issubset(counted):
                    if phase != 2 or (phase == 2 and ((x + 1) % 2, (y + 1) % 8) in locations):
                        # Add the accounted for pair to the set of counted mill potentials
                        counted |= {(x, (y + 2) % 8), (x, y)}
                        mill_count += 1

        return mill_count

    # Check how many pieces are blocked from moving anywhere on the board
    def blocked_pieces(self, locations):
        # Track the number of blocked pieces found
        blocked = 0

        for loc in locations:
            x, y = loc

            # The piece is located at the middle of a line on the board
            if y % 2 == 1 and {((x - 1) % 3, y), (x, (y - 1) % 8), (x, (y + 1) % 8)}.issubset(locations):
                blocked += 1

            # The piece is located at the corner of a square on the board
            if y % 2 == 0 and {(x, (y - 1) % 8), (x, (y + 1) % 8)}.issubset(locations):
                blocked += 1


        return blocked

    # Estimate the utility of the game if needed
    def evaluate(self, player):
        # Consider the number of pieces each player has off the board for an estimated value in phase 1
        off_board_advantage = (self.max_pieces - self.min_pieces) / (self.max_pieces + self.min_pieces) if\
            (self.max_pieces + self.min_pieces) else 0

        # Consider the number of pieces each player has on the board for an estimated value otherwise
        on_board_advantage = (len(self.max_loc) - len(self.min_loc)) / (len(self.max_loc) + len(self.min_loc)) if \
            (len(self.max_loc) + len(self.min_loc)) else 0

        # Consider the number of mills each player already has available
        mill_advantage = (self.has_mill(self.max_loc) - self.has_mill(self.min_loc)) / \
                         (self.has_mill(self.max_loc) + self.has_mill(self.min_loc)) if \
            (self.has_mill(self.max_loc) + self.has_mill(self.min_loc)) else 0

        # Consider the number of blocked opponent pieces each player has
        blocked_opponent_advantage = (self.blocked_pieces(self.min_loc) - self.blocked_pieces(self.max_loc)) / \
                                     (self.blocked_pieces(self.min_loc) + self.blocked_pieces(self.max_loc)) if \
        (self.blocked_pieces(self.min_loc) + self.blocked_pieces(self.max_loc)) else 0

        # Consider the number of possible mills each player has depending on the game phase
        possible_mill_advantage = 0
        # We are in phase 1
        if self.max_pieces > 0:
            possible_mill_advantage = (self.one_to_mill(self.max_loc, 1) - self.one_to_mill(self.min_loc, 1)) / \
                                       (self.one_to_mill(self.max_loc, 1) + self.one_to_mill(self.min_loc, 1)) if \
                (self.one_to_mill(self.max_loc, 1) + self.one_to_mill(self.min_loc, 1)) else 0

        # We are past phase 1
        else:
            possible_mill_advantage = (self.one_to_mill(self.max_loc, 2) - self.one_to_mill(self.min_loc, 2)) / \
                         (self.one_to_mill(self.max_loc, 2) + self.one_to_mill(self.min_loc, 2)) if \
                (self.one_to_mill(self.max_loc, 2) + self.one_to_mill(self.min_loc, 2)) else 0

        # Consider the mills and likely mills available to a player
        mills = 0
        likely_mills = 0

        if player.maximizes():
            mills += self.has_mill(self.max_loc)

            if self.max_pieces > 0:
                likely_mills += self.one_to_mill(self. max_loc, 1)

            else:
                likely_mills += self.one_to_mill(self.max_loc, 2)
        else:
            mills += self.has_mill(self.min_loc)

            if self.min_pieces > 0:
                likely_mills += self.one_to_mill(self.min_loc, 1)

            else:
                likely_mills += self.one_to_mill(self.min_loc, 2)

        # return an estimate that uses a weighted sum and average value
        return (off_board_advantage + on_board_advantage + (mills * 2) + likely_mills + (mill_advantage * 3) + (possible_mill_advantage * 2)
                + blocked_opponent_advantage) / 10

    # Determine a player's options when they can only move to adjacent locations
    def phase2_moves(self, locations):
        moves = list()

        # Check each location of the ones given for adjacent slots in the available spaces
        for loc in locations:
            sq, in_sq = loc
            # Pieces can move to their left or right
            potential_spaces = {(sq, (in_sq - 1) % 8), (sq, (in_sq + 1) % 8)}

            # The piece is at a square side's midpoint and can also move up or down
            if in_sq % 2 == 1:
                potential_spaces.add(((sq - 1) % 2, in_sq))

            # Of the potential spaces, find those actually available
            available_spaces = self.spaces & potential_spaces

            # Add the available spaces to our list of moves
            for new_pos in available_spaces:
                new_sq, new_in_sq = new_pos

                # Add a four tuple to allow switching positions
                moves.append((sq, in_sq, new_sq, new_in_sq))

        return moves

    # Return a list of possible moves for the game
    def moves(self):
        # If the players still have pieces not on the board, they may place them anywhere on the board where
        # there is empty space
        if (self.min_pieces > 0 and self.max_pieces > 0) or \
            (self.last_player.maximizes() and self.min_pieces > 0) or \
                ((not self.last_player.maximizes()) and self.max_pieces > 0):
            possible_moves = [a for a in self.spaces]
            return possible_moves

        # If the players have all their pieces on the board:
        # If the players have more than 2 pieces on the board, they can only move their pieces to adjacent positions
        if self.min_pieces == 0 and self.last_player.maximizes() and len(self.min_loc) > 2:
            return self.phase2_moves(self.min_loc)

        if self.max_pieces == 0 and (not self.last_player.maximizes()) and len(self.max_loc) > 2:
            return self.phase2_moves(self.max_loc)

        # If the players only have two pieces on the board, they cannot move anywhere
        if (self.last_player.maximizes() and len(self.min_loc) == 2) or \
                ((not self.last_player.maximizes()) and len(self.max_loc) == 2):
            return list()

    # Helper functions to check for 3-in-a-row as a result of a move (known as mills)
    def isMill(self, locations, move):
        # Get the location of the added piece
        if len(move) == 2:
            sq, in_sq = move
        else:
            x, y, sq, in_sq = move

        # Define subsets of possible mills to check if they are in the set of locations given
        left_mill = {(sq, (in_sq - 2) % 8), (sq, (in_sq - 1) % 8), (sq, in_sq)}
        right_mill = {(sq, in_sq), (sq, (in_sq + 1) % 8), (sq, (in_sq + 2) % 8)}
        center_mill = {(sq, in_sq - 1), (sq, in_sq), (sq, in_sq + 1)}

        # The piece is at a square's corner
        if in_sq % 2 == 0 and (left_mill.issubset(locations) or right_mill.issubset(locations)):
            return True

        # The piece is at a square side's midpoint
        elif in_sq % 2 == 1 and (center_mill.issubset(locations)):
            return True

        return False

    def mills(self, game, move):
        # We are checking if the player has a mill or not, then returning a board possibly modified as a result
        board = game.board
        player = game.last_player
        max_loc = game.max_loc
        min_loc = game.min_loc

        if player.maximizes() and self.isMill(max_loc, move):
            # Take one of the min's pieces off the board
            space_square, space_pos_in_square = min_loc.pop()
            board[space_square][space_pos_in_square] = ' '

        elif (not player.maximizes()) and self.isMill(min_loc, move):
            # Take one of the max's pieces off the board
            space_square, space_pos_in_square = max_loc.pop()
            board[space_square][space_pos_in_square] = ' '

        return SixMensMorris(board, player, game.max_pieces, game.min_pieces, max_loc, min_loc)

    # Return this game's child created by a move of a given player
    def child(self, move, player):
        # Copy the board representation for modification
        new_board = deepcopy(self.board)

        # Copy the location sets for both max and min for modification
        new_max_loc = self.max_loc.copy()
        new_min_loc = self.min_loc.copy()

        # Copy the number of pieces for both max and min for modification
        new_max_pieces = self.max_pieces
        new_min_pieces = self.min_pieces

        # Unpack move based on its length (four tuples are for moving pieces already on the board to a new location)
        if len(move) == 2:
            # We are only moving a piece onto the board
            square, pos_in_square = move

            if player.maximizes():
                new_board[square][pos_in_square] = 'A'
                new_max_pieces -= 1
                new_max_loc.add(move)

            else:
                new_board[square][pos_in_square] = 'I'
                new_min_pieces -= 1
                new_min_loc.add(move)

        else:
            # We are moving a piece already on the board to a new position
            init_square, init_pos_in_square, new_square, new_pos_in_square = move

            # Remove the piece from its original position on the board
            new_board[init_square][init_pos_in_square] = ' '

            if player.maximizes():
                new_board[new_square][new_pos_in_square] = 'A'
                new_max_loc.remove((init_square, init_pos_in_square))
                new_max_loc.add((new_square, new_pos_in_square))

            else:
                new_board[new_square][new_pos_in_square] = 'I'
                new_min_loc.remove((init_square, init_pos_in_square))
                new_min_loc.add((new_square, new_pos_in_square))

        game = SixMensMorris(new_board, player, new_max_pieces, new_min_pieces, new_max_loc,
                             new_min_loc)

        # Check for mills as a result of the move and modify the board accordingly
        return self.mills(game, move)

    # Print the game in the console
    def display(self):
        print(self.board[0][0], '-' * 9, self.board[0][1], '-' * 9, self.board[0][2])
        print('|   ', ' ' * 6, '|', ' ' * 6, '   |')
        print('|   ', self.board[1][0], '-' * 4, self.board[1][1], '-' * 4, self.board[1][2], '   |')
        print('|   ' * 2, ' ' * 7, '   |' * 2)
        print(self.board[0][7], '-', self.board[1][7], ' ' * 13,
              self.board[1][3], '-', self.board[0][3], )
        print('|   ' * 2, ' ' * 7, '   |' * 2)
        print('|   ', self.board[1][6], '-' * 4, self.board[1][5], '-' * 4, self.board[1][4], '   |')
        print('|   ', ' ' * 6, '|', ' ' * 6, '   |')
        print(self.board[0][6], '-' * 9, self.board[0][5], '-' * 9, self.board[0][4])
