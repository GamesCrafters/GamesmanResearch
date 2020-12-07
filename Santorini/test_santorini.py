from solver import *
from game_santorini import *

tables = [[], []]

# starting position
positions = [Position()]
visited = set()
visited.add(Hash(positions[0]))

# run DFS
while positions:
    curr = positions.pop()
    s = Solve(curr)
    while len(tables[0]) <= s[1]:
        tables[0].append({"win": 0, "lose": 0, "tie": 0, "total": 0})
        tables[1].append({"win": 0, "lose": 0, "tie": 0, "total": 0})
    t = curr.turn()
    tables[t][s[1]][s[0]] += 1
    tables[t][s[1]]["total"] += 1

    if PrimitiveValue(curr) == "not_primitive":
        for m in GenerateMoves(curr):
            new = DoMove(curr, m)
            if Hash(new) not in visited:
                positions.append(new)
                visited.add(Hash(new))

def printf(a, b, c, d, e):
    print(("{:<8}"*5).format(a, b, c, d, e))

for i in range(2):
    table = tables[i]
    printf("Remote", "Win", "Lose", "Tie", "Total")
    print('-'*40)
    tw = tl = tt = tto = 0
    for i in range(len(table)-1,-1,-1):
        w, l, t, to = table[i]["win"], table[i]["lose"], table[i]["tie"], table[i]["total"]
        printf(i, w, l, t, to)
        tw += w
        tl += l
        tt += t
        tto += to
    print('-'*40)
    printf("Total", tw, tl, tt, tto)
