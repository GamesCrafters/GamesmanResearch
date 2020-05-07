#include <stdint.h>
#include <stdlib.h>
/*
#include "loa.c"
#include "HashMap.c"
#include "Kruskal.c"
#include "UnionFind.c"
#include "Queue.c"
*/
//0 is Lose, 1 is Win, 2 is Tie, 3 is PrimLose, 4 is PrimTie
void solver(struct table* memory,int* position) {
    int value = PrimitiveValue(position);
    if ((value == 3) && (lookup(memory,position) == -1)) {
        insert(memory,position,3);
        return;
    } else if (value == 4) {
        insert(memory,position, 4);
        return;
    }
    int* MoveList = GenerateMoves(position);
    int tieFlag = 0;
    int* NewPosition;
    for (int i = 1; i < *(MoveList); i = i + 4) {
        NewPosition = DoMove(position, *(MoveList+i),*(MoveList+i+1),*(MoveList+i+2),*(MoveList+i+3));
        //Checked Store is the Symmetry Checker
        CheckStored(memory,NewPosition);
        if (lookup(memory,NewPosition) == -1) {
            solver(memory,NewPosition);
        }
        if (lookup(memory,NewPosition) == 1) {
            insert(memory,position, 0);
            return;
        }
        if ((lookup(memory,NewPosition) == 2) || (lookup(memory,NewPosition) == 4)) {
            tieFlag = 1;
        }
        free(NewPosition);
    }
    if ((lookup(memory,position) == -1) || tieFlag) {
        insert(memory, position,2);
        return;
    }
    insert(memory,position,0);
}
