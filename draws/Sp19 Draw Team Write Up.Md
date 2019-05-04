Gamesman Purity Check Write Up
Matthew Pearson, Ajay Kosuri, Karan Shah

Files: openpositions.c, openpositions.h, minor changes to textui.c and analysis.c

Most Important Functions: DeterminePure, DeterminePure1, SetDrawParents, PrintDrawAnalysis

Location: Purity Check is at the bottom of openPositions.c (In GamesmanClassic/src/core) separated by a block of empty lines

Goal: To isolate and mark pure draw games
 
Description: This semester we made an addition to the Gamesman solver so that any loopy game will now allow the user to learn
             if the game is a pure draw game (no loses on any draw level that point to another lose). We started by locating 
             code relevant to solving loopy games in the solver and then understanding it. We then used the code from 
             solveloopy.c in the bottom of openpositions.c where we then modified it to serve our purpose. Currently, the 
             purity check solves the game calculating draw wins and draw loses and their draw level and then runs a check to 
             see if any draw loses point to a draw lose. While checking whether or not the code worked, there were multiple 
             errors found in the python solver and we traced out the multi-file logic to debug and add the requisite 
             corrections so that the solver would perform as necessary. At the conclusion of the semester, we were able 
             to deliver on the purity check for Gamesman games, added multiple fixes to the python solver, and made an 
             addition to the game analysis table that includes draw wins, draw loses, and the total number of positions for 
             each draw level.
 
Results: We found that the majority of draw games were not pure draws, with the exception of Ataxx, Blocking, Horseshoe, 
         Pong Hau Ki, and Tile Chess (within games in the Gamesman solver). Blocking, Horseshoe and Pong Hau Ki are all the 
         same games.
 
Bugs: The purity check does not work on multi-tier games, possibly due to unhandled tier hashing conflicts within 
      multi-tier solving. But for non-tier games, to get the result of whether the game is a pure-draw, we need to first solve 
      the game (command ‘s’) and then run the purity check (command ‘r’). For Tier-Games, we can toggle whether those games use 
      the tier solver (command 't') to make it act as if it is a non-tier game. This, however, does not work for Nine Men’s 
      Morris which exclusively has a tier solver (possibly an area for improvement in the future). Currently, the solver 
      will only show up for games which can be solved so if the interaction with tier games is to be solved whoever is 
      working on it must also change textui.c.
 
Future: In the future, we hope to make an option to make a pure solver so that we can store the draw level along with the 
        regular data from the solver. This would allow us to perform a simple look-up while running purity check after the 
        game is solved once and this could also lead to an improvement to the Gamesman AI so that it plays more competitively 
        using the data from draw levels.

WORK BREAKDOWN:
Matt: Coding and project lead, ran purity and draw check on some games, code for draw analysis
 
Ajay: minor help coding, majority of writeup, ran purity check on some games, ran draw check on games, code for draw analysis
 
Karan: Understanding the files, tracing execution thread and debugging solver, ran purity check on portion of games,
       refined final write-up
