from Game import Game
from PrimitiveValues import PrimitiveValues
import math


class TicTacToe(Game):

    def __init__(self, len, wid, win):
        assert len > 0
        assert wid > 0
        assert win > 0
        self.length = len
        self.width = wid
        self.size = self.length * self.width
        self.num = win
        self.start, self.winX, self.winO = "", "", ""
        for i in range(len * wid):
            self.start += "-"
        for i in range(win):
            self.winX += "X"
            self.winO += "O"
        self.biases = []
        for i in range(self.size // 2):
            self.biases.append(self.rearranger(i, i))
            self.biases.append(self.rearranger(i + 1, i))

    def do_move(self, p, m):
        return p[:m[1]] + m[0] + p[m[1] + 1:]

    def generate_moves(self, p):
        x, o = 0, 0
        blanks = []
        for i in range(len(p)):
            if p[i] == "X":
                x += 1
            elif p[i] == "O":
                o += 1
            else:
                blanks.append(i)
        if x == o:
            return [("X", i) for i in blanks]
        return [("O", i) for i in blanks]

    def primitive_value(self, p):
        for i in range(0, self.width):
            row = p[i * self.length: (i + 1) * self.length]
            if row == self.winX or row == self.winO:
                return PrimitiveValues.LOSE
        for i in range(0, self.length):
            col = p[i::self.length]
            if col == self.winX or col == self.winO:
                return PrimitiveValues.LOSE
        if self.num <= min(self.length, self.width):
            d1, d2, d3, d4 = "", "", "", ""
            for i in range(self.num):
                d1 += p[self.length * self.width - 1 - (i * self.length + i)]
                d2 += p[self.length * self.width - 1 - ((i + 1) * self.length - i - 1)]
                d3 += p[i * self.length + i]
                d4 += p[(i + 1) * self.length - i - 1]
            diagonals = [d1, d2, d3, d4]
            for d in diagonals:
                if d == self.winX or d == self.winO:
                    return PrimitiveValues.LOSE
        if "-" not in p:
            return PrimitiveValues.TIE
        return PrimitiveValues.UNDECIDED

    def convert1Dto2D(self, p):
        matrix = []
        for i in range(self.width):
            row = []
            for j in range(self.length):
                row.append(p[i * self.length + j])
            matrix.append(row)
        return matrix

    def convert2Dto1D(self, matrix):
        position = ""
        for i in range(self.width):
            for j in range(self.length):
                position += matrix[i][j]
        return position

    def rotate(self, p):
        list_of_tuples = zip(*self.convert1Dto2D(p)[::-1])
        return self.convert2Dto1D([list(elem) for elem in list_of_tuples])

    def reflect(self, p):
        matrix = self.convert1Dto2D(p)
        for i in range(self.width):
            matrix[i] = matrix[i][::-1]
        return self.convert2Dto1D(matrix)

    def hash(self, p):
        x, o = 0, 0
        for i in range(len(p)):
            if p[i] == "X":
                x += 1
            elif p[i] == "O":
                o += 1
        return self.rearranger(x, o)

    def rearranger(self, x, o):
        return math.factorial(self.size) / math.factorial(x) / math.factorial(o) / math.factorial(self.size - x - o)
