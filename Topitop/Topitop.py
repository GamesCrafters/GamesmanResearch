from Game import Game
from PrimitiveValues import PrimitiveValues


def do_move_helper(p, t, m):
    src = m[0]
    dest = m[1]
    if type(src) == str:  # new piece placed from off the board
        if src == "R" or src == "B":
            assert src == t
        p[dest] = src + p[dest]
    else:  # move piece already on the board
        p[dest] = p[src] + p[dest]
        p[src] = ""
    return p


class Topitop(Game):

    def __init__(self, b, s, l, mis, blue, row, col, win):
        self.buckets = b  # number of buckets per player
        self.small = s  # number of available small sand piles
        self.large = l  # number of available large sand piles
        self.misere = mis  # true if misere variation
        self.blue_first = blue  # true if blue goes first
        self.rows = row  # number of rows on board
        self.cols = col  # number of cols on board
        self.size = row * col  # number of spaces on board
        self.positions = []  # list of positions explored
        self.fringe = []  # list of positions to be explored
        self.num_win = win  # number of sand castles with buckets on top needed to win
        assert self.small >= self.num_win
        assert self.large >= self.num_win
        assert self.buckets >= self.num_win

    def do_move(self, p, m):
        curr_p = p[0]
        prev_p = p[1]
        turn = p[2]
        new_p = do_move_helper(curr_p.copy(), turn, m)
        assert new_p != prev_p
        if turn == "R":  # swap turns
            return new_p, curr_p, "B"
        else:
            return new_p, curr_p, "R"

    def generate_moves(self, p):
        red, blue, small, large = 0, 0, 0, 0
        moves = []
        curr_p = p[0]
        prev_p = p[1]
        turn = p[2]

        for i in range(self.size):
            space = curr_p[i]
            adj = self.get_adjacent_indices(i)
            if space == "":  # empty space
                continue

            # count number of pieces on the board
            if "R" in space:
                red += 1
            if "B" in space:
                blue += 1
            if "S" in space:
                small += 1
            if "L" in space:
                large += 1

            for j in adj:
                if space[0] == turn:  # top piece is a bucket of player's color
                    if space[-1] == turn and (curr_p[j] == "" or curr_p[j][0] == "S"):
                        # moving only bucket to empty space or space with small sand pile on top
                        moves.append((i, j))
                    elif space[-1] == "S" and (curr_p[j] == "" or curr_p[j][0] == "L"):
                        # moving bucket piece to empty space or space with large sand pile only
                        moves.append((i, j))
                    elif space[-1] == "L" and curr_p[j] == "":
                        # moving sand castle to empty space
                        moves.append((i, j))
                elif space[0] == "S":  # top piece is a small sand pile
                    if space[-1] == "S" and (curr_p[j] == "" or curr_p[j][0] == "L"):
                        # moving small sand pile to empty space or space with large sand pile only
                        if do_move_helper(curr_p.copy(), turn, (i, j)) != prev_p:  # can't reverse opponent's move
                            moves.append((i, j))
                    elif space[-1] == "L" and curr_p[j] == "":
                        # moving castle piece to empty space
                        if do_move_helper(curr_p.copy(), turn, (i, j)) != prev_p:  # can't reverse opponent's move
                            moves.append((i, j))
                elif space == "L" and curr_p[j] == "":
                    # moving large sand pile to empty space
                    if do_move_helper(curr_p.copy(), turn, (i, j)) != prev_p:  # can't reverse opponent's move
                        moves.append((i, j))

        # number of available pieces off the board
        assert red <= self.buckets
        assert blue <= self.buckets
        assert small <= self.small
        assert large <= self.large
        red_avail, blue_avail = self.buckets - red, self.buckets - blue
        small_avail, large_avail = self.small - small, self.large - large

        # possible pieces that could be placed onto board
        for i in range(self.size):
            space = curr_p[i]
            if red_avail > 0 and turn == "R" and space == "":  # place red bucket onto empty space
                moves.append(("R", i))
            if blue_avail > 0 and turn == "B" and space == "":  # place blue bucket onto empty space
                moves.append(("B", i))
            if small_avail > 0 and space == "":  # place small sand pile onto empty space
                moves.append(("S", i))
            if large_avail > 0 and space == "":  # place large sand pile onto empty space
                moves.append(("L", i))

        return moves

    # computes the indices of valid adjacent spaces on the board given the index of a space on the board
    def get_adjacent_indices(self, index):
        adj = []
        row = index // self.cols
        col = index % self.cols
        if row > 0 and col > 0:  # upper left
            adj.append((row - 1) * self.cols + col - 1)
        if row > 0:  # straight up
            adj.append((row - 1) * self.cols + col)
        if row > 0 and col < self.cols - 1:  # upper right
            adj.append((row - 1) * self.cols + col + 1)
        if col > 0:  # straight left
            adj.append(row * self.cols + col - 1)
        if col < self.cols - 1:  # straight right
            adj.append(row * self.cols + col + 1)
        if row < self.rows - 1 and col > 0:  # lower left
            adj.append((row + 1) * self.cols + col - 1)
        if row < self.rows - 1:  # straight down
            adj.append((row + 1) * self.cols + col)
        if row < self.rows - 1 and col < self.cols - 1:  # lower right
            adj.append((row + 1) * self.cols + col + 1)
        return adj

    def primitive_value(self, p):
        red_castles, blue_castles = 0, 0
        curr_p = p[0]
        turn = p[2]
        for i in range(self.size):
            if curr_p[i] == "RSL":  # red sand castle
                red_castles += 1
            elif curr_p[i] == "BSL":  # blue sand castle
                blue_castles += 1
        if not self.misere and (  # original rules
                (turn == "R" and blue_castles == self.num_win) or (turn == "B" and red_castles == self.num_win)):
            return PrimitiveValues.LOSE
        elif self.misere and (  # misere variation
                (turn == "R" and red_castles == self.num_win) or (turn == "B" and blue_castles == self.num_win)):
            return PrimitiveValues.LOSE
        return PrimitiveValues.UNDECIDED

    def count(self):
        if self.blue_first:
            turn = "B"
        else:
            turn = "R"
        self.fringe.append((["" for _ in range(self.size)], None, turn))  # empty starting board
        counter = 0
        while len(self.fringe) > 0:  # there are still new positions to explore
            p = self.fringe.pop(0)
            self.positions.append(p)
            counter += 1
            if self.primitive_value(p) == PrimitiveValues.UNDECIDED:  # game hasn't ended
                moves = self.generate_moves(p)
                for m in moves:
                    new_p = self.do_move(p, m)
                    if new_p not in self.positions:  # new position
                        self.fringe.append(new_p)
        print("Number of Positions: ", len(self.positions))


game1 = Topitop(2, 4, 4, False, True, 3, 3, 2)
game1.count()
