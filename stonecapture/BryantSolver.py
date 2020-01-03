### Beauty and Joy of Computing
###
### Game Solver
###
### By Prof. Dan Garcia, UC Berkeley

LOSE      = "Lose"
WIN       = "Win"
TIE       = "Tie"
UNDECIDED = "Undecided"
DRAW = "Draw"

WHITE = "White"
BLACK = "Black"

class goBoardGraph:
    def __init__(self,size):
        self.size = size
        self.position = {}
        for i in range(self.size*self.size):
            self.position[str(i)] = []
            # print(i)
            if (i % self.size) != 0:
                self.position[str(i)].append(str(i-1))
                # print("left")
            if (i + 1) <= (((i // size) + 1) * size) - 1:
                # print("right")
                self.position[str(i)].append(str(i+1))
            if (i + self.size) <= (self.size*self.size - 1):
                # print("bottom")
                self.position[str(i)].append(str(i+self.size))
            if (i - self.size >= 0):
                # print("top")
                self.position[str(i)].append(str(i-self.size))

            # if (i % self.size) != 0 and (i + self.size) <= (self.size*self.size - 1):
            #     print("bottom left")
            #     self.position[str(i)].append(str(i - 1 + self.size))

            # if (i % self.size) != 0 and (i - self.size >= 0):
            #     print("top left")
            #     self.position[str(i)].append(str(i - 1 - self.size))

            # if (i + 1) <= (((i // size) + 1) * size) - 1 and (i + self.size) <= (self.size*self.size - 1):
            #     print("bottom right")
            #     self.position[str(i)].append(str(i + self.size + 1))
            # if (i + 1) <= (((i // size) + 1) * size) - 1 and (i - self.size >= 0):
            #     print("top right")
            #     self.position[str(i)].append(str(i + 1 - self.size))



position = "2010011001000000"

class scgo_game:

    def __init__(self, size, limit):
        self.size = size
        self.boardgraph = goBoardGraph(self.size)
        # print(self.boardgraph.position)
        self.limit = limit
        self.edges = ["0", "1", "2", "3", "4", "7", "8", "11", "12", "15" ]
        self.dict = {}

    def primitive(self, position):
        "Return value {WIN, LOSE, TIE} if POSITION is a primitive (game over), otherwise UNDECIDED"

        blackvals = len([x for x in range(len(position[1:])) if (int(position[1:][x]) == 1)])
        whitevals = len([x for x in range(len(position[1:])) if (int(position[1:][x]) == 2)])

        if blackvals >= self.limit:
            return WIN
        elif whitevals >= self.limit:
            return LOSE
        else: 
            return UNDECIDED
        # if blackvals > whitevals:
        #     return WIN
        # elif blackvals == whitevals:
        #     return TIE
        # else:
        #     return LOSE


    def generate_moves(self, position):
        "Return all the moves available from POSITION"
        pos = position[1:]
        return [x for x in range(len(pos)) if (int(pos[x]) == 0)]
        
        #return (1,) if position == 1 else (1,2)

    def do_move(self, position, move):
        "Return the child position resulting from doing the MOVE from the POSITION"
        player = position[0]
        lst = list(position[1:])
        op = "1" if player == "2" else "2"  
        if player == "2" and not self.is_surrounded("".join(lst), str(move), player):
            lst[int(move)] = "2"
        elif player == "1" and not self.is_surrounded("".join(lst), str(move), player):
            lst[int(move)] = "1"
        else:
            return "".join([op] + lst)
        
        

        new_pos = "".join(lst)
        # print(new_pos)

        
        op_pieces = [str(x) for x in range(self.size * self.size) if lst[x] == op] 
        op_p_copy = op_pieces.copy()
        removepls = []
        count = 0
        # print(op_p_copy)
        # print(len(op_pieces))
        while len(op_p_copy) != 0 and count < len(op_pieces):
            dr = op_p_copy.pop()
            # print(dr)
            stuff = self.is_surrounded(new_pos, dr, op)
            # print(stuff)
            if stuff:
                removepls += stuff
                for i in stuff[1:]:

                    op_p_copy.remove(i)
            count += 1
        # print(removepls)
        for i in removepls:
            lst[int(i)] = "0"
        lst = [op] + lst
        return "".join(lst)

    # def print_board(position, size):
    #     pos = list(position[1:])
    #     for i in range(len(pos)):
    #         if i % size == 0:
                


        

        

    # def enclosed(self, position, move, player):
    #     lst = position.split()
    #     playerpos = []
    #     newplayerpos = []
    #     if player == WHITE:
    #         piece = "2"
    #     else:
    #         piece = "1"
    #     for i in range(len(lst)):
    #         if lst[i] == piece:
    #             playerpos.append(i)
    #             newplayerpos.append(i)
    #     newplayerpos.append(move)

    def is_surrounded(self, position, coord, player):
        lst = list(position)
        if player == "2":
            piece = "2"
        else:
            piece = "1"
        # print(lst)

        visited = [False] * (len(self.boardgraph.position)) 
  
        # Create a queue for BFS 
        queue = [] 
  
        # Mark the source node as  
        # visited and enqueue it 
        queue.append(str(coord)) 
        visited[int(coord)] = True
        cont_count = 1
        piece_list = [ str(x) for x in range(len(lst)) if lst[x] == piece]
        visited_pieces = [str(coord)]
        while queue and cont_count < 6: 
  
            # Dequeue a vertex from  
            # queue and print it 
            # print("this is q: ", queue)
            s = queue.pop(0) 
            # print (s, end = " ") 
            
            # Get all adjacent vertices of the 
            # dequeued vertex s. If a adjacent 
            # has not been visited, then mark it 
            # visited and enqueue it 
            # print(s, " is parent")
            # print(self.boardgraph.position[s])
            for i in self.boardgraph.position[s]: 
                # print(i, " is child")
                # print(visited[int(i)] == False and (lst[int(i)] == piece or lst[int(i)] == "0"))
                if visited[int(i)] == False and (lst[int(i)] == piece or lst[int(i)] == "0"):
                    # print(int(i), " was visited")
                    # print(visited_pieces)
                    # print(lst[int(i)]  in visited_pieces)
                    if lst[int(i)] == piece and (int(i) not in visited_pieces):
                        visited_pieces.append(str(i))
                    cont_count += 1
                    queue.append(str(i)) 
                    visited[int(i)] = True
        # print(visited_pieces)
        if cont_count < 6:
            return visited_pieces
        else:
            return False

    # def edges_reached(self, position, player, start):
    #     lst = list(position)
    #     if player == WHITE:
    #         piece = "2"
    #     else:
    #         piece = "1"
    #     pieces = [ str(x) for x in range(len(lst)) if lst[x] == piece]
    #     visited = [False] * (len(self.boardgraph.position)) 
    #     # Create a queue for BFS 
    #     queue = [] 
    #     # Mark the source node as  
    #     # visited and enqueue it 
    #     queue.append(start) 
    #     visited[int(start)] = True
    #     visited_edges = []
    #     print(pieces)
    #     # print(visited)
    #     while queue: 
  
    #         # Dequeue a vertex from  
    #         # queue and print it 
    #         s = queue.pop(0) 
    #         # print (s, end = " ") 
  
    #         # Get all adjacent vertices of the 
    #         # dequeued vertex s. If a adjacent 
    #         # has not been visited, then mark it 
    #         # visited and enqueue it 
    #         for i in self.boardgraph.position[s]: 
    #             # print(i)

    #             if visited[int(i)] == False and i in pieces: 
    #                 queue.append(i) 
    #                 print(i)
    #                 if i in self.edges and i not in visited_edges:
    #                     visited_edges.append(i)
    #                 visited[int(i)] = True
    #     return visited_edges
        
    def solver(self, position, dct, draw):
        prim = self.primitive(position)
        if position in dct:
            return dct[position]
        if prim != UNDECIDED:
            dct[position] = prim
        elif draw > 50:
            prim = DRAW
        else:
            lst = [self.solver(self.do_move(position, move,), dct, draw + 1) for move in self.generate_moves(position) ]  
            prim = WIN if LOSE in lst else (DRAW if DRAW in lst else LOSE)
        return prim

        
        

        




    # def solve(position):
    #     "Solve the game (walk the tree starting from POSITION), return value {WIN, LOSE, TIE}"
    #     if primitive(position) != UNDECIDED:
    #         return primitive(position)
    #     else:
    #         values = [solve(do_move(position,move)) for move in generate_moves(position)]
    #         return WIN if LOSE in values else (TIE if TIE in values else LOSE)

    # def dot(position):
    #     "Walk the tree and print the DOT information"
    #     seen = {}
    #     def dot_helper(position):
    #         "Help walk the game tree starting from POSITION"
    #         if position in seen:
    #             return
    #         if primitive(position) != UNDECIDED:
    #             seen[position] = None
    #             return
    #         else:
    #             for move in generate_moves(position):
    #                 seen[position] = None
    #                 child = do_move(position,move)
    #                 print(str(position) + " -> " + str(child))
    #                 dot_helper(child)

    #     print("digraph G {")
    #     dot_helper(position)
    #     print("}")

    # dot(4)

    # for p in range(10,-1,-1):
    #     print(str(p)+"\'s value:"+solve(p))
b = scgo_game(4,8)
strtpos = "10000000000000000"