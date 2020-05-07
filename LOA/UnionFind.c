#include <stdlib.h>
/*
#include "Kruskal.c"
*/
struct Set {
    int size;
    int* parent;
    int* rank;
};

struct Set* MakeSet(int size) {
    struct Set* s = (struct Set*) malloc(sizeof(struct Set));
    s->size = size;
    s->parent = (int*) malloc(sizeof(int) * size);
    s->rank = (int*) malloc(sizeof(int)*size);
    for (int i = 0; i < size; i++) {
        s->parent[i] = i;
        s->rank[i] = 0;
    }
    return s;
}

int Find(struct Set* s, int vertex) {
    if (s->parent[vertex] != vertex) {
        s->parent[vertex] = Find(s,s->parent[vertex]);
    }
    return s->parent[vertex];
}
void Union(struct Set* s,int x, int y) {
    int xRoot = Find(s,x);
    int yRoot = Find(s,y);
    if (xRoot == yRoot) {
        return;
    }
    if (s->rank[xRoot] < s->rank[yRoot]) {
        int temp = xRoot;
        xRoot = yRoot;
        yRoot = temp;
    }
    s->parent[yRoot] = xRoot;
    if (s->rank[xRoot] == s->rank[yRoot]) {
        s->rank[xRoot] = s->rank[xRoot] + 1;
    }
    return;
}
void freeUnionSet(struct Set* s) {
    free(s->parent);
    free(s->rank);
    free(s);
    return;
}

//
// Created by Max Gilchrist on 3/13/20.
//

