#include <stdlib.h>
struct Node {
    struct Edge* data;
    struct Node* next;
};
struct Queue{
    int size;
    struct Node* root;
};
struct Queue* CreateQueue() {
    struct Queue* q = (struct Queue*) malloc(sizeof(struct Queue));
    struct Node* n = malloc(sizeof(struct Node));
    n->data->weight = 0;
    n->next = NULL;
    q->root = n;
    q->size = 0;
    return q;
}
void InsertElement(struct Queue* q, struct Edge new) {
    struct Node* n = malloc(sizeof(struct Node));
    struct Edge* e = malloc(sizeof(struct Edge));
    *e = new;
    n->data = e;
    struct Node* temp = q->root;
    while((temp->next != NULL) && (temp->next->data->weight < n->data->weight)){
        temp = temp->next;
    }
    n->next = temp->next;
    temp->next = n;
    q->size += 1;
}
struct Edge* GetNext(struct Queue* q) {
    struct Edge* value = q->root->next->data;
    free(q->root->next);
    q->root->next = q->root->next->next;
    return value;
}
//
// Created by Max Gilchrist on 3/13/20.
//

