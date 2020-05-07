#include <stdlib.h>
#include "loa.c"
#include "solver.c"
#include "HashMap.c"
#include "Kruskal.c"
#include "UnionFind.c"
#include "Queue.c"
int* InitPos() {
    int* position = malloc(sizeof(int)*64);
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (((i == 0) && ((0 < j ) && (j < 7))) || ((i == 7) && ((0 < j ) && (j < 7)))) {
                *(position + (8*i)+j) = 2;
            } else if (((j == 0) && ((0 < i ) && (i < 7))) || ((j == 7) && ((0 < i ) && (i < 7)))){
                *(position + (8*i)+j) = 3;
            } else {
                *(position + (8*i)+j) = 0;
            }
        }
    }
    return position;
}
int main() {
    int* First_Position = InitPos();
    struct table* memory = makeTable();
    solver(memory, First_Position);
    return 0;
}
