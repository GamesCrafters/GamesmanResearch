#include <stdlib.h>
#include <inttypes.h>
struct node{
    int key;
    int val;
    struct node* next;
};
struct table{
    int size;
    struct node** list;
};
struct table *makeTable(int size) {
    struct table* t = (struct table*) malloc(sizeof(struct table));
    t->size = size;
    t->list = (struct node**)malloc(sizeof(struct node*)*size);
    for (int i = 0; i < size; i++) {
        t->list[i] = NULL;
    }
    return t;
}
int Hash(int* position) {
    __int128_t hash = 0b0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++)
            hash = (*(position+(i*8)+j) << (2*(8*i+j))) | (hash);
    }
    return hash;
}
int indexFinder(struct table* t, int key) {
    return key%t->size;
}
void insert(struct table* t, int* key , int val) {
    //Possible hashing improvments
    //pos = hashReduce

    int hashedKey = Hash(key);
    int pos = indexFinder(t,hashedKey);
    struct node* list = t->list[pos];
    struct node* newNode = (struct node*) malloc(sizeof(struct node));
    struct node* temp = list;
    while(temp) {
        if (temp->key == hashedKey) {
            temp->val = val;
            return;
        }
        temp = temp->next;
    }
    newNode->key = hashedKey;
    newNode->val = val;
    newNode->next = list;
    t->list[pos] = newNode;
}
int lookup(struct table *t, int* key) {
    //pos = hashReduce
    int hashedKey = Hash(key);
    int pos = indexFinder(t,hashedKey);
    struct node *list = t->list[pos];
    struct node *temp = list;
    while(temp) {
        if (temp->key == hashedKey) {
            return temp->val;
        }
        temp = temp->next;
    }
    return -1;
}