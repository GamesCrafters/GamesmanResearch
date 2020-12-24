from PrimitiveValues import PrimitiveValues
from TicTacToe import TicTacToe as TTT
import time


class DPSolver:

    def __init__(self, g):
        self.game = g
        self.memo = [PrimitiveValues.UNDECIDED for _ in range(sum(self.game.biases))]
        self.primitiveCounter = [0, 0, 0, 0, 0, 0]
        self.counter = [0, 0, 0, 0, 0, 0]

    def solve(self):
        for i in range(sum(self.game.biases) - 1, -1, -1):
            pos = self.game.unhash(i)
            value = self.game.primitive_value(pos)
            if value == PrimitiveValues.UNDECIDED:
                children = [self.memo[self.game.hash(self.game.do_move(pos, m), True)] for m in self.game.generate_moves(pos)]
                if PrimitiveValues.LOSE in children:
                    value = PrimitiveValues.WIN
                elif PrimitiveValues.TIE in children:
                    value = PrimitiveValues.TIE
                elif PrimitiveValues.DRAW in children:
                    value = PrimitiveValues.DRAW
                else:
                    value = PrimitiveValues.LOSE
            self.memo[i] = value
        return self.memo[0]


times = []
for _ in range(10):
    game = TTT(3, 3, 3)
    experiment = DPSolver(game)
    start = time.perf_counter()
    experiment.solve()
    end = time.perf_counter()
    times.append(end - start)
print("Average Time: ", sum(times) / len(times))
