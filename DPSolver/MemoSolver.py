from PrimitiveValues import PrimitiveValues
from TicTacToe import TicTacToe as TTT
import time


class MemoSolver:

    def __init__(self, g):
        self.game = g
        self.memo = {}
        self.primitiveCounter = [0, 0, 0, 0, 0, 0]
        self.counter = [0, 0, 0, 0, 0, 0]

    def solve(self, p, tief):
        if p in self.memo:
            v = self.memo[p]
        else:
            v = (self.game.primitive_value(p), 0)
            if v[0] is PrimitiveValues.UNDECIDED:
                children = [self.solve(self.game.do_move(p, m), tief) for m in self.game.generate_moves(p)]
                values = [c[0] for c in children]
                if PrimitiveValues.LOSE in values:
                    v = (PrimitiveValues.WIN, min([c[1] for c in children if c[0] == PrimitiveValues.LOSE]) + 1)
                elif PrimitiveValues.TIE in values:
                    v = (PrimitiveValues.TIE, tief([c[1] for c in children if c[0] == PrimitiveValues.TIE]) + 1)
                elif PrimitiveValues.DRAW in values:
                    v = (PrimitiveValues.DRAW, -1)
                elif PrimitiveValues.WIN in values:
                    v = (PrimitiveValues.LOSE, max([c[1] for c in children if c[0] == PrimitiveValues.WIN]) + 1)
                else:
                    v = (PrimitiveValues.INVALID, -1)
            else:
                self.primitiveCounter[v[0].value] += 1
            self.memo[p] = v
            self.counter[v[0].value] += 1
        return v


times = []
for _ in range(100):
    game = TTT(3, 3, 3)
    experiment = MemoSolver(game)
    start = time.perf_counter()
    experiment.solve(game.start, min)
    end = time.perf_counter()
    times.append(end - start)
print("Average Time: ", sum(times) / len(times))
