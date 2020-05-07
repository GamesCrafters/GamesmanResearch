#include <math.h>
/*
#include "UnionFind.c"
#include "Queue.c" */
int factorial(int n) {
    if (n == 1) {
        return 1;
    }
    return n*factorial(n-1);
}
struct Graph{
    int VertexNumber;
    int ESize;
    struct Edge* E;
};

struct Edge{
    int u;
    int v;
    int weight;
};

/*
struct Edge CreateEdge(int u0, int u1,int u, int v0, int v1, int v) {
    struct Edge new;
    new.first = u;
    new.second = v;
    new.weight = Distance(u0,u1,v0,v1);
    return new;
}
*/

struct Graph CreateGraph(int* position) {
    struct Graph G;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (*(position+(8*i)+j) == 3) {
                G.VertexNumber += 1;
            }
        }
    }
    int n = 0;
    int xPosition[G.VertexNumber];
    int yPosition[G.VertexNumber];
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (*(position+(8*i)+j) == 3) {
                xPosition[n] = i;
                yPosition[n] = j;
                n++;
            }
        }
    }
    n = factorial(G.VertexNumber);
    G.ESize = n;
    struct Edge E[G.ESize];
    int a = 0;
    for (int i = 0; i < G.VertexNumber - 1; i++) {
        for (int j = i + 1; j < G.VertexNumber; j++) {
            E[a].u = i;
            E[a].v = j;
            E[a].weight = (int) floor(sqrt(((xPosition[i]-xPosition[j])*(xPosition[i]-xPosition[j] )) + (yPosition[i]-yPosition[j])*(yPosition[i]-yPosition[j])));
        }
    }
    return G;
}
//Return 0 for not Solved return 1 for solved
int MSTWeight(int* position) {
    struct Graph G = CreateGraph(position);
    struct Queue* q = CreateQueue();
    struct Set* s = MakeSet();
    for (int i = 0; i < G.ESize; i++) {
        InsertElement(q,G.E[i]);
    }
    //Figure out the unionfind implementation
    //First we start by putting all of the pieces into a disjoint set struct.
    //find
    int n = 0;
    struct Edge e;
    while(n != G.VertexNumber - 1) {
        e = GetNext(q);
        if (e.weight != 1) {
            return 0;
        }
        if (Find(Helper(s,e.u)) != Find(Helper(s,e.v))) {
            totalWeight += e.weight;
            Union(s,Helper(s,e.u),Helper(s,e.v));
            n += 1;
        }
    }
    return 1;
}
//
// Created by Max Gilchrist on 3/13/20.
//

