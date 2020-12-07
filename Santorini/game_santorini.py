# Game constants
# --------------
W = 2
H = 3
# --------------

'''
We define a position as the location of all 4 player pieces, as well as the height of each square (0-4).
This results in (W*H)^4 * 4^(W*H) possible hashes.
'''

class Position:
    def __init__(self):
        self.board = [[0]*W for _ in range(H)]
        self.pieces = [(0, -1) for _ in range(4)]

    def copy(self):
        pos = Position()
        for r in range(H):
            for c in range(W):
                pos.board[r][c] = self.board[r][c]
        for i in range(4):
            pos.pieces[i] = self.pieces[i]
        return pos

    def turn(self):
        return sum(sum(r) for r in self.board) % 2

pow4 = [4**i for i in range(W*H+1)]
powWH = [(W*H+1)**i for i in range(4)]
def Hash(pos):
    ans = 0
    for i in range(W*H):
        r = i // W
        c = i % W
        ans += pos.board[r][c] * pow4[i]
    ans2 = 0
    for i in range(4):
        p = pos.pieces[i][0] * W + pos.pieces[i][1] + 1
        ans2 += p * powWH[i]

    return ans + ans2 * pow4[W*H]

def Unhash(hash):
    ans = hash % pow4[W*H]
    ans2 = hash // pow4[W*H]
    pos = Position()
    for i in range(W*H):
        r = i // W
        c = i % W
        pos.board[r][c] = ans % 4
        ans //= 4
    for i in range(4):
        curr = ans2 % (W*H+1)
        ans2 //= (W*H+1)
        curr -= 1
        pos.pieces[i] = (0, -1) if curr < 0 else (curr // W, curr % W)

    return pos

def DoMove(pos, move):
    newpos = pos.copy()

    # place new player (1 tuple)
    if len(move) == 1:
        for i in range(4):
            if pos.pieces[i] == (0, -1):
                newpos.pieces[i] = move[0]
                break
    # move and place (3 tuples)
    # piece start, piece end, block pos
    elif len(move) == 3:
        for i in range(4):
            if pos.pieces[i] == move[0]:
                newpos.pieces[i] = move[1]
                newpos.board[move[2][0]][move[2][1]] += 1
                break

    return newpos

dr = [-1,-1,-1, 0, 0, 1, 1, 1]
dc = [-1, 0, 1, -1,1,-1, 0, 1]
def GenerateMoves(pos):
    moves = []

    # placing pieces
    for i in range(4):
        if pos.pieces[i] == (0, -1):
            for r in range(H):
                for c in range(W):
                    if (r, c) not in pos.pieces:
                        moves.append([(r, c)])
            return moves

    R = [0,1] if pos.turn() == 0 else [2,3]
    for i in R:
        # move
        for d1 in range(8):
            r, c = pos.pieces[i]
            nr1, nc1 = r + dr[d1], c + dc[d1]
            if 0 <= nr1 < H and 0 <= nc1 < W and 4 != pos.board[nr1][nc1] < pos.board[r][c] + 2 \
            and (nr1, nc1) not in pos.pieces:
                # place
                for d2 in range(8):
                    nr2, nc2 = nr1 + dr[d2], nc1 + dc[d2]
                    if 0 <= nr2 < H and 0 <= nc2 < W and pos.board[nr2][nc2] != 4 \
                    and ((nr2, nc2) not in pos.pieces or (nr2, nc2) == (r, c)):
                        moves.append([(r, c), (nr1, nc1), (nr2, nc2)])

    return moves

def ExistMoves(pos):
    # placing pieces
    for i in range(4):
        if pos.pieces[i] == (0, -1):
            return True

    R = [0, 1] if pos.turn() == 0 else [2, 3]
    for i in R:
        # move
        for d1 in range(8):
            r, c = pos.pieces[i]
            nr1, nc1 = r + dr[d1], c + dc[d1]
            if 0 <= nr1 < H and 0 <= nc1 < W and 4 != pos.board[nr1][nc1] < pos.board[r][c] + 2 \
                    and (nr1, nc1) not in pos.pieces:
                # place
                for d2 in range(8):
                    nr2, nc2 = nr1 + dr[d2], nc1 + dc[d2]
                    if 0 <= nr2 < H and 0 <= nc2 < W and pos.board[nr2][nc2] != 4 \
                            and ((nr2, nc2) not in pos.pieces or (nr2, nc2) == (r, c)):
                        return True

    return False

def PrimitiveValue(pos):
    if any(pos.board[p[0]][p[1]] == 3 for p in pos.pieces):
        return "lose"
    if not ExistMoves(pos):
        return "lose"
    return "not_primitive"
