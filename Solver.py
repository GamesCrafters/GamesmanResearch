
def all_positions(initial_position):
    all_ps, old_all_ps, cur_positions = [initial_position], [], [initial_position]
    while all_ps != old_all_ps:
        old_all_ps, using_cur_pos, cur_positions = all_ps[:], cur_positions[:], []
        for pos in using_cur_pos:
            for child in down_child(pos):
                if child not in all_ps:
                    all_ps += [child]
                    if primitive(child) ==  'UNDECIDED':
                        cur_positions += [child]
    return all_ps

def solve(position):
    if primitive(position) != 'UNDECIDED':
        return primitive(position)
    else:
        moves = generate_moves(position)
        child_ends = []
        for move in moves:
            child_ends.append(solve(do_move(position, move)))
        if 'LOSE' in child_ends:
            return 'WIN'
        else:
            return 'LOSE'

def up_solve(position):
    mover = {}
    for p in all_positions(position):
        mover[p] = primitive(p)
    ol_mover = {}
    while mover != ol_mover:
        ol_mover = dict(mover)
        for undecided_pos in [p for p in list(mover.keys()) if mover[p] == 'UNDECIDED']:
            solve_child = [mover[p] for p in down_child(undecided_pos)]
            if "LOSE" in solve_child:
                mover[undecided_pos] = 'WIN'
            elif 'TIE' in solve_child:
                mover[undecided_pos] = 'TIE'
            elif 'UNDECIDED' not in solve_child:
                mover[undecided_pos] = 'LOSE'                
    for key in list(mover.keys()):
        if mover[key] == 'UNDECIDED':
            mover[key] = 'DRAW'
    return mover

def up_solve_draw_world_one_tier(position):
    mover = {}
    for p in all_positions(position):
        mover[p] = primitive(p)
    ol_mover = {}
    while mover != ol_mover:
        ol_mover = dict(mover)
        for undecided_pos in [p for p in list(mover.keys()) if mover[p] == 'UNDECIDED']:
            solve_child = [mover[p] for p in down_child(undecided_pos)]
            if "LOSE" in solve_child:
                mover[undecided_pos] = 'WIN'
            elif 'TIE' in solve_child:
                mover[undecided_pos] = 'TIE'
            elif 'UNDECIDED' not in solve_child:
                mover[undecided_pos] = 'LOSE'                
    for key in list(mover.keys()):
        if mover[key] == 'UNDECIDED':
            mover[key] = 'DRAW '
    Number_of_draws = 1
    while 'DRAW ' * Number_of_draws in mover.values() and Number_of_draws < 100:
        for po in [p for p in mover.keys() if mover[p] == ('DRAW ' * Number_of_draws)]:
            solve_child = [mover[p] for p in down_child(po)]
            if ('DRAW ' * (Number_of_draws-1)) + 'WIN' in solve_child:
                mover[po] += 'LOSE'
        ol_mover = {}
        while ol_mover != mover:
            ol_mover = dict(mover)
            for draw_pos in [p for p in list(mover.keys()) if mover[p] == ('DRAW ' * Number_of_draws)]:
                s_child = [mover[p] for p in down_child(draw_pos)]
                if ("DRAW " * Number_of_draws) + "LOSE" in s_child:
                    mover[draw_pos] = mover[draw_pos] + 'WIN'
                elif ("DRAW " * Number_of_draws) + "TIE" in s_child:
                    mover[draw_pos] = mover[draw_pos] + 'TIE'
                elif ("DRAW " * Number_of_draws) not in s_child:
                    mover[draw_pos] = mover[draw_pos] + 'LOSE'
        for key in list(mover.keys()):
            if mover[key] == ('DRAW ' * Number_of_draws):
                mover[key] += 'DRAW '
        Number_of_draws += 1
    return mover
us = up_solve_draw_world_one_tier

def aminax(minmax, lst):
    if lst:
        return minmax(lst)
    else:
        return -1

def up_remote(su, aps):
    remoteness_dic, ol_remoteness_dic = {}, {}
    for p in aps:
        if primitive(p) != 'UNDECIDED':
            remoteness_dic[p] = 0
        elif su[p] not in ['WIN', 'LOSE', 'TIE']:
            remoteness_dic[p] = float('inf')
        else:
            remoteness_dic[p] = 'UNDECIDED'
    while ol_remoteness_dic != remoteness_dic:
        ol_remoteness_dic = dict(remoteness_dic)
        for p in [_ for _ in remoteness_dic if su[_] in ['WIN', 'LOSE', 'TIE'] and primitive(_) == 'UNDECIDED']:
            WL, children = su[p], [q for q in down_child(p) if remoteness_dic[q] != 'UNDECIDED']
            if WL == 'WIN':
                remoteness_dic[p] = aminax(min, [remoteness_dic[_] for _ in children if su[_] == 'LOSE']) + 1
            elif WL == 'TIE':
                remoteness_dic[p] = aminax(min, [remoteness_dic[_] for _ in children if su[_] == 'TIE']) + 1
            elif WL == 'LOSE':
                remoteness_dic[p] = aminax(max, [remoteness_dic[_] for _ in children if su[_] == 'WIN']) + 1
    return remoteness_dic

def draw_remote(su, aps):
    remoteness_dic, ol_remoteness_dic = {}, {}
    for p in aps:
        if su[p] in ['WIN', 'LOSE', 'TIE']:
            remoteness_dic[p] = 0
        elif 'WIN' in child_solver(p, su):
            remoteness_dic[p] = 1
        else:
            remoteness_dic[p] = 'UNDECIDED'
    while ol_remoteness_dic != remoteness_dic:
        ol_remoteness_dic = dict(remoteness_dic)
        for p in [q for q in remoteness_dic if su[q] not in ['WIN', 'LOSE', 'TIE'] and 'WIN' not in child_solver(q, su)]:
            WL, children = su[p], [q for q in down_child(p) if remoteness_dic[q] != 'UNDECIDED']
            if WL == 'DRAW WIN':
                remoteness_dic[p] = aminax(min, [remoteness_dic[q] for q in children if su[q] == 'DRAW LOSE']) + 1
            elif WL == 'DRAW LOSE':
                remoteness_dic[p] = aminax(max, [remoteness_dic[q] for q in children if su[q] == 'DRAW WIN']) + 1
    return remoteness_dic

def remotenessN(su, n):
    remoteness_dic, ol_remoteness_dic = {}, {}
    avoidList = []
    for l in ["WIN", "LOSE", "TIE"]:
        for i in range(n):
            avoidList.append("DRAW " * i + l)
    for p in list(su.keys()):
        if su[p] in avoidList:
            remoteness_dic[p] = 0
        elif 'DRAW ' * (n - 1) + "WIN" in child_solver(p, su):
            remoteness_dic[p] = 1
        else:
            remoteness_dic[p] = 'UNDECIDED'
    while ol_remoteness_dic != remoteness_dic:
        ol_remoteness_dic = dict(remoteness_dic)
        for p in [q for q in remoteness_dic if su[q] not in avoidList and 'DRAW ' * (n - 1) + "WIN" not in child_solver(q, su)]:
            WL, children = su[p], [q for q in down_child(p) if remoteness_dic[q] != 'UNDECIDED']
            if WL == 'DRAW ' * n + "WIN":
                remoteness_dic[p] = aminax(min, [remoteness_dic[q] for q in children if su[q] == 'DRAW ' * n + "LOSE"]) + 1
            elif WL == 'DRAW ' * n + "LOSE":
                remoteness_dic[p] = aminax(max, [remoteness_dic[q] for q in children if su[q] == 'DRAW ' * n + "WIN"]) + 1
    return remoteness_dic

def allRemote(su):
    largest = 0
    for v in su.values():
        largest = max(numDraws(v), largest)
    remotenessDic = up_remote(su, su.keys())
    for i in range(largest):
        justInts = [remotenessDic[m] for m in su.keys() if type(remotenessDic[m]) is int and remotenessDic[m] != float('inf')]
        curLargest = max(justInts)
        trd = remotenessN(su, i + 1)
        for m in [m for m in remotenessDic.keys() if type(remotenessDic[m]) is str or remotenessDic[m] == float('inf') and type(trd[m]) is int and trd[m] != 0]:
            remotenessDic[m] = trd[m] - 1#+ curLargest + 1
    return remotenessDic

def allRemoteGLOBAL(su):
    largest = 0
    for v in su.values():
        largest = max(numDraws(v), largest)
    remotenessDic = up_remote(su, su.keys())
    for i in range(largest):
        justInts = [remotenessDic[m] for m in su.keys() if type(remotenessDic[m]) is int and remotenessDic[m] != float('inf')]
        curLargest = max(justInts)
        trd = remotenessN(su, i + 1)
        for m in [m for m in remotenessDic.keys() if type(remotenessDic[m]) is str or remotenessDic[m] == float('inf') and type(trd[m]) is int]:
            remotenessDic[m] = trd[m] + curLargest + 1
    return remotenessDic

def bestDrawPlayer(Position, primitive, generateMoves, doMove, downChild, printBoard, solved={}, remote={}):
    if solved == {}:
        solved = up_solve_draw_world_one_tier(Position)
    if remote == {}:
        remote = allRemoteGLOBAL(solved)
    moves = downChild(Position)
    SP = solved[Position]
    #print()
    #print(remote[Position])
    #print(SP)
    if SP[len(SP) - 3:] == "WIN":
        lookingFor = "OSE"
    elif SP[len(SP) - 3] == "TIE":
        lookingFor = "TIE"
    else:
        lookingFor = "WIN"
    SPM = [solved[m] for m in moves]
    nmoves = [m for m in moves if lookingFor == solved[m][len(solved[m]) - 3:]]
    #print([solved[r] for r in moves])
    #print([remote[r] for r in moves])
    if lookingFor == "WIN":
        largestRm = 0
        for n in nmoves:
            if remote[n] > largestRm:
                largestRm = remote[n]
                m = n
    else:
        largestRm = max(remote.values()) + 1
        for n in nmoves:
            if remote[n] < largestRm:
                largestRm = remote[n]
                m = n
    #if primitive(m) == "UNDECIDED":
    #    return bestDrawPlayer(m, primitive, generateMoves, doMove, downChild, printBoard, solved, remote)
    return m
    #except:
    #    print("")
    #except InfiniteRecursionError:
    #    print

def play(position=None, solved=None, r=None, verbose=True, superVerbose=False, human_turn=True, rG=None):
    if position == None:
        position = START_POS
    if solved == None:
        solved = s
    if r == None:
        r = allRemote(solved)
    if rG == None:
        rG = allRemoteGLOBAL(solved)
    print()
    if r[position] == 0 and numDraws(solved[position]) == 0:
        print("Game over")
        if not human_turn:
            print("YOU", primitive(position))
        else:
            print("you", primitive(position))
        return
    if not human_turn:
        print("You gave computer this board")
    if verbose:
        print("Value:", solved[position], "     Remoteness", r[position], "     Draw level", numDraws(solved[position]))
    print(position)
    if human_turn:
        mvs = generate_moves(position)
        for m in range(len(mvs)):
            if superVerbose:
                npt = do_move(position, mvs[m])
                print(m, mvs[m], "This will give them a position with V:", solved[npt], "R:", r[npt], "DL:", numDraws(solved[npt]))
            else:
                print(m, mvs[m])
        validI = False
        while not validI and human_turn:
            i = input("Type the number next to the move you want to make. > ")
            if i == "-v":
                verbose = not verbose
                print("verbose is now", verbose)
            elif i == "-sv":
                superVerbose = not superVerbose
                print("superVerbose is now", superVerbose)
            else:
                try:
                    j = int(i)
                    if j >= 0 and j < len(mvs):
                        validI = True
                    else:
                        print("That is an invalid number please try again")
                except ValueError:
                    print("Please type a number")
        m = mvs[j]
        np = do_move(position, m)
    else:
        np = bestDrawPlayer(position, primitive, generate_moves, do_move, down_child, print, solved, rG)
    if numDraws(solved[position]) != numDraws(solved[np]) and verbose:
        print()
        if numDraws(solved[position]) > numDraws(solved[np]):
            print("HAHA You have fallen from draw level", numDraws(solved[position]), "to draw level", numDraws(solved[np]))
        else:
            print("HAHA You have risen from draw level", numDraws(solved[position]), "to draw level", numDraws(solved[np]), "when you had control of the game")
    if solved[position][len(solved[position]) - 3:] == "WIN" and solved[np][len(solved[np]) - 3:] == "WIN":
        print("HAHA you have given up control of the game")
    return play(position=np, solved=solved, r=r, verbose=verbose, superVerbose=superVerbose, human_turn=not human_turn, rG=rG)

r = allRemote(s)
rG = allRemoteGLOBAL(s)
play()