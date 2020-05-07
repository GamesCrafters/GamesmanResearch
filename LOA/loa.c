#include <stdlib.h>
#include <stdint.h>

//store white as 0b10 and black as 0b11
/*
#include "HashMap.c"
#include "Kruskal.c"
#include "Queue.c"
#include "UnionFind.c"*/
//We need a distance function d(x,y) that
//


void Transpose(int* position) {
    int temp;
    for (int i = 0; i < 7; i++) {
        for (int j = i + 1; j < 8; j++) {
            temp = *(position+(8*i)+j);
            *(position+(8*i)+j) = *(position+(8*j)+i);
            *(position+(8*j)+i) = temp;
        }
    }
}
void Flip(int* position) {
    int temp = 0;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 8; j++) {
            temp = *(position+(i*8)+j);
            *(position+(i*8)+j) = *(position+((7-i)*8)+j);
            *(position+((7-i)*8)+j) = temp;
        }
    }
}
void Rotate90(int* position) {
    Transpose(position);
    Flip(position);
}

void CheckStored(struct table* memory, int* position) {
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    Flip(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    if (lookup(memory,position) != -1) {
        return;
    }
    Rotate90(position);
    Flip(position);
}
void FlipColors(int* position) {
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (*(position+(i*8)+j) == 2) {
                *(position+(i*8)+j) = 3;
            } else if (*(position+(i*8)+j) == 3) {
                *(position+(i*8)+j) = 2;
            }
        }
    }
}

//for a move [x0,y0,x1,y1]
int* DoMove(int* position, int x0, int y0, int x1, int y1) {
    int* NewPosition = (int*) malloc(sizeof(int) * 64);
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            *(NewPosition+(8*i)+j) = *(position+(8*i)+j);
        }
    }
    *(NewPosition+(8*x0) + y0) = 0;
    *(NewPosition+(8*x1) + y1) = 2;
    FlipColors(NewPosition);
    return NewPosition;
}
int inBounds(int x, int y) {
    if ((x < 0) || (x > 7) || (y < 0) || (y > 7)) {
        return 0;
    }
    return 1;
}
/* Overview of what I want to do here.
 * So the main loop is gonna be search for places that have a 2 on the,
 * then when it finds one the valid pieces
 * we need to check each of the directions
 * 111   000  001
 * 110        010
 * 101   100  011
 *
 */

int* GenerateMoves(int* position) {
    //The player moving is always 2
    int n = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (*(position+(8*i)+j) == 2) {
                n += 1;
            }
        }
    }
    int xPosition[n];
    int yPosition[n];
    n = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (*(position+(8*i)+j) == 2) {
                xPosition[n] = i;
                yPosition[n] = j;
                n++;
            }
        }
    }
    int directstore[3*n + 1];
    directstore[0] = n;
    int numMoves = 0;
    int diag;
    int hori;
    int vert;
    int x; int y;
    int a; int b;
    for (int i = 0; i < n; i++) {
        diag = 0; hori = 0; vert = 0;
	x = xPosition[i]; y = yPosition[i];
        for (int j = 0; j < 8; j++) {
            if (*(position + (8*j) + y) != 0) {
                hori += 1;
            }
        }
        for (int j = 0; j < 8; j++) {
            if (*(position + (8*x) + j) != 0) {
                vert += 1;
            }
        }
        if (x < y) {
            a = 0; b = y-x;
            for (int j = 0; j < (7-(y-x));j++) {
                if (*(position+(8*a)+b) != 0) {
                    diag != 1;
                    a += 1;
                    b += 1;
                }
            }
        } else {
            a = x-y; b = 0;
            for (int j = 0; j < (7-(y-x));j++) {
                if (*(position+(8*a)+b) != 0) {
                    diag != 1;
                    a += 1;
                    b += 1;
                }
            }
        }
        directstore[1+(3*i)] = hori;
        directstore[2+(3*i)] = vert;
        directstore[3+(3*i)] = diag;
    }
    //Need to check if it is a valid position
    int templist[8*n];
    int z = 0;
    for (int i = 0; i < n; i++) {
        a = xPosition[i]; b = yPosition[i];
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            b++;
            z++;
            
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            b--;
            z++;
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            a++;
            z++;
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            a--;
            z++;
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            a++;
            b++;
            z++;
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            a++;
            b--;
            z++;
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            a--;
            b--;
            z++;
        }
        while (inBounds(a,b) && (*(position+(8*a)+b) == 3)) {
            a--;
            b++;
            z++;
        }
    }
    return MoveList;
}


int PrimitiveValue(int* position) {
    //0 is Lose, 1 is Win, 2 is Tie, 3 is PrimLose, 4 is PrimTie, 5 is Not Primitive
    int* MoveList = GenerateMoves(position);
    if (*(MoveList) == 0) {
        return 4;
    }
    int MSTweight = MSTWeight(position);
    if (MSTweight == 0) {
        return 3;
    } else {
        return 5;
    }
}
