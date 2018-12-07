Draws write up - Matthew Pearson

Files : Solver.py

Most Important Functions: up_solve_draw_world_one_tier(StartPos) --nicknamed us, allRemote(), bestDrawPlayer(), play(), isPure(), numDraws()

Definitions:
  Fringe: A draw position that contains a move that would cause someone to drop a draw Level.
                     These positions are allowed to have moves that allow you to forcibly increase the remoteness despite not having
                     control of the game.
                     These positions are allowed to have moves that point to other drawLoses in the fringe assuming the game isn't pure.
  Draw Level: The minimum number of mistakes nessecary to be made to cause a game over. 
                    If you don't understand, think about it like this:
                    Assume you try to solve a game and get a group of positions that are draws.
                    Then you create a new game that only contains those draws and redefine primitive return true if position is on the 
                      fringe of the old game.
                    Try to solve the new game.
                    The draw level of a position is the number of times you have to do this process before the position gets removed.
  Control: If you are at a winning position, doesn't care what draw level you are at.
  Draw N Lose: A loseing position in draw level N.
                    written as DRAW DRAW LOSE in my solver for draw level 2. DRAW DRAW DRAW LOSE for draw level 3. etc.
  Draw N Win: A winning position in draw level N.
                    The same as Draw N Lose but with Wins.
  Pure: determines if a game has any DrawLoses that point to other draw Loses.
                    Overrides the Fringe position condition of Draw N Loses pointing to other Draw N Loses on the fringe and instead
                        requires that no Draw N Lose points to ANY other Draw N Lose.
                   

For my work this semester I tried to study the draws of games and everything about them. I started by working on a way to visualize
the draw world of games. This caused me to write a function that takes a solved game and prints out the code that could be used to create
GraphViz visualization of this solved game. Thats the function def printViz(solved_dic, remoteness_dic, max_remoteness). Once this was
done it became clear that some games fit a certain pattern that, assuming you define all fringe-level positions to be DrawLoses, no
DrawLose points to another DrawLose, much like the rule in Draw Level 0, aka the real non draw world. I could work far more in-depth for
all pure games. Some small pure games I found were PongHauKi, and Mu Torere. My solver I created a year ago solves the game in entirety,
meaning that just because I keep solving the game for all draw levels so every single position is assigned a win, lose, or tie no matter
the draw level or purity. Once this game is solved, I can find the remoteness of each position relative to its draw level, or to the global
remoteness level. With this information I can create a perfect computer player, play(), that is cocky and laughs at you if you make any
kind of mistake. Play() takes advantage of all my functions up to this point is the culmination of my work this semester studying draws.

I am proud to say that I, Matthew Pearson, solved games more in depth than ever before in gamesCrafters and can have my software laugh
at a user, typically me, if they mess up during a game.
