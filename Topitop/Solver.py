from PrimitiveValues import PrimitiveValues


class Solver:

    def __init__(self, g, symmetries):
        self.game = g
        self.memo = {}
        self.primitiveCounter = [0, 0, 0, 0, 0, 0]
        self.counter = [0, 0, 0, 0, 0, 0]
        self.sym = symmetries

    def solve(self, p, tief):
        symmetries = []
        if self.sym:
            symmetries = [p, self.game.reflect(p)]
            for i in range(3):
                symmetries.append(self.game.rotate(symmetries[-2]))
                symmetries.append(self.game.rotate(symmetries[-2]))
            symmetries = list(set(symmetries).intersection(self.memo.keys()))
        if len(symmetries) > 0:
            v = self.memo[set(symmetries).intersection(self.memo.keys()).pop()]
        elif not self.sym and p in self.memo:
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

    def analyze(self):
        values = self.memo.values()
        print("{:<8s}{:<8s}{:<8s}{:<8s}{:<8s}".format("Remote", "Win", "Lose", "Tie", "Total"))
        print("-" * 37)
        total_wins, total_losses, total_ties = 0, 0, 0
        for i in range(max([v[1] for v in values]), -1, -1):
            remote = [v[0] for v in values if v[1] == i]
            wins = remote.count(PrimitiveValues.WIN)
            total_wins += wins
            ties = remote.count(PrimitiveValues.TIE)
            total_ties += ties
            losses = remote.count(PrimitiveValues.LOSE)
            total_losses += losses
            print("{:<8d}{:<8d}{:<8d}{:<8d}{:<8d}".format(i, wins, losses, ties, wins + ties + losses))
        print("-" * 37)
        print("{:<8s}{:<8d}{:<8d}{:<8d}{:<8d}".format("Total", total_wins, total_losses, total_ties,
                                                      total_wins + total_losses + total_ties))