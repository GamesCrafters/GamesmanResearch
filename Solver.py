# Functions required of all games: primitive(position), generate_moves(position), do_move(position, move)
# Variables required of all games: START_POS    --This can be removed if someone wants to clean up the functions play() and printViz()
# Function required for PrintViz: stringify(position)
# If you plan to use lists in your implementations of your positions or moves DONT. Use Tuples instead. Lists will cause errors.

# Returns all the positions that one can get to from a given position
# Inputs: The position you want to get the children of.
def down_child(position):
    return [do_move(position, m) for m in generate_moves(position)]

# Returns all possible positions that can be reached from the certain position of a game, typically the start_pos
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

# Solves a position of a game. Assumes no draws in the game from the position and below
# Inputs: the position you want to solve for.
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

# Solves a game for draw level 0 and returns a dictionary [position : value]. The values are "WIN", "LOSE", "TIE", and "DRAW".
# values cannot be anything besides one of the four listed
# Inputs: the initial position of the game.
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

# solves the whole game in entirety and returns a dictionary of [position : value]. Every position is given Win Lose Tie and Draw Level
# format described for value is the python operation of "DRAW" * N + "WIN OR LOSE OR TIE" where N is the Draw Level of the position.
# Ex format: "DRAW DRAW LOSE"
# Inputs: the initial position of the game
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

# helper function that makes calculating remoteness in up_remote much easier. Returns -1 so that we can get a remoteness of zero
# if primitive or the best possible remoteness given the possible values. Best is determined by the function minmax which is just either
# the min function or the max function
# Inputs: minmax = either the min function or the max function, lst = a list of remotenesses that are still subject to change.
def aminax(minmax, lst):
    if lst:
        return minmax(lst)
    else:
        return -1

# Returns a dictionary of [position : Remoteness] for all positions of draw level 0. All other positions are in the dictionary but have
# remoteness float('inf')
# Inputs: su = a dictionary of type [position : value] where the values are of the format that return from up_solve_draw_world_one_tier,
#              where the value also holds information about the draw level, or of the type that come from up_solve(), where the values 
#              are limited, but up_solve_draw_world_one_tier just gives more information so it is better and preferred.
def up_remote(su):
    remoteness_dic, ol_remoteness_dic = {}, {}
    for p in su.keys():
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

# A function that returns a dictionary of [position : remoteness] for all position in draw level 1 where the remoteness of the fringe 
# of draw level 1 is 0. all other positions are in there and if the other positions have draw level 0 then their value is 0 and if
# the other positions have draw level >= 2 their value is "UNDECIDED"
# Inputs: su = a dictionary of type [position : value] where the values are of the format that return from up_solve_draw_world_one_tier,
#              where the value also holds information about the draw level.
def draw_remote(su):
    remoteness_dic, ol_remoteness_dic = {}, {}
    for p in su.keys():
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

# A function that returns a dictionary of [position : remoteness] for all position in draw level N where the remoteness of the fringe 
# of draw level N is 0. all other positions are in there and if the other positions have draw level < N then their value is 0 and if
# the other positions have draw level > N their value is "UNDECIDED". This function is a strict upgrade from draw_remote()
# Inputs: su = a dictionary of type [position : value] where the values are of the format that return from up_solve_draw_world_one_tier,
#              where the value also holds information about the draw level.
#         n = the draw level you want to solve for.
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

# Returns a dictionary of type [position : remoteness] that gives a remoteness to all values in the game relative to their draw level.
# The preferred function for remoteness relative to draw level. EX) all fringe positions of any draw level have remoteness 0
# Much more useful for conceptual understanding of game trees and the play function than allRemoteGLOBAL().
# Inputs: su = a dictionary of type [position : value] where the values are of the format that return from up_solve_draw_world_one_tier,
#              where the value also holds information about the draw level.
def allRemote(su):
    largest = 0
    for v in su.values():
        largest = max(numDraws(v), largest)
    remotenessDic = up_remote(su)
    for i in range(largest):
        justInts = [remotenessDic[m] for m in su.keys() if type(remotenessDic[m]) is int and remotenessDic[m] != float('inf')]
        curLargest = max(justInts)
        trd = remotenessN(su, i + 1)
        for m in [m for m in remotenessDic.keys() if type(remotenessDic[m]) is str or remotenessDic[m] == float('inf') and type(trd[m]) is int and trd[m] != 0]:
            remotenessDic[m] = trd[m] - 1
    return remotenessDic

# Returns a dictionary of type [position : remoteness] that gives a remoteness to all values in the game relative to the global count.
# The preferred function for remoteness relative to the global count. To further explain the global count, the remoteness relative to 
# draw level is the same as normal, but the fringe of draw level N isn't just 0, it is (the max remoteness of Draw level N-1) + 2.
# between each draw level there will be a remoteness value that is empty that is used to note the moving of draw level.
# Much more useful for creating graph visualizations with printViz and bestDrawPlayer mocking than allRemote().
# Could be improved to run faster by using a combination of numDraws and allRemote.
# Inputs: su = a dictionary of type [position : value] where the values are of the format that return from up_solve_draw_world_one_tier,
#              where the value also holds information about the draw level.
def allRemoteGLOBAL(su):
    largest = 0
    for v in su.values():
        largest = max(numDraws(v), largest)
    remotenessDic = up_remote(su)
    for i in range(largest):
        justInts = [remotenessDic[m] for m in su.keys() if type(remotenessDic[m]) is int and remotenessDic[m] != float('inf')]
        curLargest = max(justInts)
        trd = remotenessN(su, i + 1)
        for m in [m for m in remotenessDic.keys() if type(remotenessDic[m]) is str or remotenessDic[m] == float('inf') and type(trd[m]) is int]:
            remotenessDic[m] = trd[m] + curLargest + 1
    return remotenessDic

# Makes a move in the game and Returns the new position of the board.
# Inputs: Position = the current position of the game.
#         solved = the dictionary of format [position : value]. MUST BE OF FORMAT FROM up_solve_draw_world_one_tier to work
#         remote = the dicitonary of format [position : remoteness]. MUST BE OF FORMAT FROM allRemoteGLOBAL to work
def bestDrawPlayer(Position, solved={}, remote={}):
    if solved == {}:
        solved = up_solve_draw_world_one_tier(Position)
    if remote == {}:
        remote = allRemoteGLOBAL(solved)
    moves = [do_move(Position, m) for m in generate_moves(Position)]
    SP = solved[Position]
    if SP[len(SP) - 3:] == "WIN":
        lookingFor = "OSE"
    elif SP[len(SP) - 3] == "TIE":
        lookingFor = "TIE"
    else:
        lookingFor = "WIN"
    SPM = [solved[m] for m in moves]
    nmoves = [m for m in moves if lookingFor == solved[m][len(solved[m]) - 3:]]
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
    return m

# A function that plays the game with one human and one computer player. The computer player is controlled by bestDrawPlayer. If
# you want to quit halfway just use keyboard force exit. Otherwise exits once game is over.
# preferred function call is play(). But if you already have access to a solved dictionary of type defined in up_solve_draw_world_one_tier
# please set solved equal to that dictionary. The same goes for r to format allRemote and rG to format allRemoteGLOBAL.
# those are not necessary precalculations but would save time on initialization.
# if you type -v during an input the verbose mode will toggle.
# if verbose is on the next position will print telling the Value, Remoteness (local), and Draw Level of the position.
# if you type -sv during an input the super Verbose mode will toggle.
# if superVerbose is on then the possible moves listed will also contain the Value, Remoteness (local), and draw level of position your
#     opponent would go to.
# Inputs: (Optional) position = the position of the current game. default is the initial position of the game
#         (Optional) solved = a dictionary of type described in up_solve_draw_world_one_tier called on the initial position of the game
#                             The variable is here to save runtime.
#         (Optional) r = a dictionary of type described in allRemote called on the initial position solved dictionary. 
#                        The only acceptable value is allRemote(up_solve_draw_world_one_tier(START_POS)).
#                        The variable is here to save on runtime.
#         (Optional) human_turn = a boolean value about whos turn it is. Human or Computer. Default is True, so Human goes first.
#         (Optional) rG = a dictionary of type described in allRemoteGLOBAL called on the initial position solved dictionary. 
#                        The only acceptable value is allRemoteGLOBAL(up_solve_draw_world_one_tier(START_POS)).
#                        The variable is here to save on runtime.
#         (Optional) printBoard = a function that nearly prints out the current position of nice viewing. Default is the print function
#         (Optional) verbose = DO NOT OVERRIDE. Variable used for storage purposes
#         (Optional) superVerbose = DO NOT OVERRIDE. Varible used for storage purposes.

def play(position=None, solved=None, r=None, human_turn=True, rG=None, printBoard=None, verbose=False, superVerbose=False):
    if position == None:
        position = START_POS
    if solved == None:
        solved = up_solve_draw_world_one_tier(position)
    if r == None:
        r = allRemote(solved)
    if rG == None:
        rG = allRemoteGLOBAL(solved)
    if printBoard == None:
        printBoard = print
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
    printBoard(position)
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
        np = bestDrawPlayer(position, solved, rG)
    if numDraws(solved[position]) != numDraws(solved[np]) and verbose:
        print()
        if numDraws(solved[position]) > numDraws(solved[np]):
            print("HAHA You have fallen from draw level", numDraws(solved[position]), "to draw level", numDraws(solved[np]))
        else:
            print("HAHA You have risen from draw level", numDraws(solved[position]), "to draw level", numDraws(solved[np]), "when you had control of the game")
    if solved[position][len(solved[position]) - 3:] == "WIN" and solved[np][len(solved[np]) - 3:] == "WIN":
        print("HAHA you have given up control of the game")
    return play(position=np, solved=solved, r=r, human_turn=not human_turn, rG=rG, printBoard=printBoard, verbose=verbose, superVerbose=superVerbose)

# Prints a bunch of code that the GraphViz bundle can understand and create a graph from.
# Inputs: s = solved dictionary of format [position : value] from up_solve_draw_world_one_tier.
#         r = remoteness dictionary of format [positon : remoteness] from allRemoteGLOBAL.
#         m = max(r.values()) just do it
def printViz(s, r, m):
    print(" digraph G {")
    print(" {")
    print("   node [shape=plaintext];")
    print()
    remoteness_line = '0;'
    for i in range(1, m + 1):
        remoteness_line = str(i) + " -> " + remoteness_line
    print(remoteness_line)
    print(' }')
    for p in s.keys():
        color = 'green' if s[p][-3:] == 'WIN' else 'red'
        shape = 'triangle' if p == START_POS else 'circle'
        print('node [fontname = "Courier",sytle=filled,color=' + color + ',shape=' + shape + ']')
        print('  "' + stringify(p) + '" [shape=circle];')
    counter = 0
    for position in s.keys():
        temp = 'temp' + str(counter)
        done = False
        print('  { rank=same; ' + str(r[position]) + '; "' + stringify(position) + '";  }')
        for parent in parents(position, s.keys()):
            if primitive(parent) == "UNDECIDED":
                print('  "' + stringify(parent) + '" -> "' + stringify(position) + '" [label=" ", color=black];')
                done = True
                counter += 1
    print('}')

# Returns the draw level of the value given.
# Inputs: val = the value of the position you want to know the draw level of.
def numDraws(val):
    num = 0
    while True:
        if (len(val) > 4 and val[:4] == "DRAW"):
            num += 1
            val = val[5:]
        else:
            return num

# Returns a boolean of whether the game is pure
# Inputs: s = solved dictionary of format [position : value] from up_solve_draw_world_one_tier
def isPure(s):
    for p in s.keys():
        if len(p) >= 4 and p[-4:] == "LOSE":
            children = child_solver(p)
            for c in children:
                if len(c) >= 4 and c[-4:] == "LOSE":
                    return False
    return True

# Returns all the values of the children of a position
# Inputs: p = a position that you want that you want to know the values of the children of.
#         su = the solved dictioary of type [position : value]. No need for any specific solver.
def child_solver(p, su):
    child_solved_list = []
    for dc in down_child(p):
        child_solved_list.append(su[dc])
    return child_solved_list
