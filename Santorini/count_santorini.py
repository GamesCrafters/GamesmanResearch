# Game constants
# ----------
W = 3
H = 3
PLAYER_PIECES = 2
MAX_LEVEL1 = 22
MAX_LEVEL2 = 18
MAX_LEVEL3 = 14
MAX_LEVEL4 = 18
# ----------


# Constrain pieces by board size
MAX_LEVEL1 = min(MAX_LEVEL1, W*H)
MAX_LEVEL2 = min(MAX_LEVEL2, W*H)
MAX_LEVEL3 = min(MAX_LEVEL3, W*H)
MAX_LEVEL4 = min(MAX_LEVEL4, W*H-2*PLAYER_PIECES)

import math
# choose
def nCr(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

# Calculate number of positions for a given tier
def calculateTier(tier):
    output = 0

    nP1 = max(0, tier - 2*PLAYER_PIECES) # Number of pieces on level 1+
    minX1 = math.ceil(nP1 / 4)
    maxX1 = min(MAX_LEVEL1, nP1)
    for x1 in range(minX1, maxX1+1):
        nP2 = nP1 - x1 # Number of pieces on level 2+
        minX2 = math.ceil(nP2 / 3)
        maxX2 = min(MAX_LEVEL2, nP2, x1)
        for x2 in range(minX2, maxX2+1):
            nP3 = nP2 - x2 # Number of pieces on level 3+
            minX3 = math.ceil(nP3 / 2)
            maxX3 = min(MAX_LEVEL3, nP3, x2)
            for x3 in range(minX3, maxX3+1):
                nP4 = nP3 - x3
                minX4 = nP4
                maxX4 = min(MAX_LEVEL4, nP4, x3)
                for x4 in range(minX4, maxX4+1):
                    # number of ways to arrange blocks
                    total = 1
                    total *= nCr(W*H, x1)
                    total *= nCr(x1, x2)
                    total *= nCr(x2, x3)
                    total *= nCr(x3, x4)
                    # number of ways to place players
                    p1 = min(tier, PLAYER_PIECES)
                    total *= nCr(W*H-x4, p1)
                    p2 = min(max(0, tier - PLAYER_PIECES), PLAYER_PIECES)
                    total *= nCr(W*H-x4-p1, p2)

                    output += total

    return output

total = 0
for t in range(MAX_LEVEL1+MAX_LEVEL2+MAX_LEVEL3+MAX_LEVEL3+6):
    c = calculateTier(t)
    total += c
    print(f'Tier {t}: \t{c}')
print('-'*10)
print(f'Total: {total}')
