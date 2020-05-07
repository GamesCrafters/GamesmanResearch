#include <stdlib.h>
#include <stdio.h>
static void flip(int* position) {
	int temp;
	for (int i = 0; i < 2; i++) {
		for (int j = 0; j < 4; j++) {
			temp = *(position+(4*i)+j);
			*(position+(4*i)+j) = *(position+(4*(3-i))+j);
			*(position+(4*(3-i))+j) = temp;
		}
	}
}
static void transpose(int* position) {
	int temp;
	for (int i = 0; i < 3; i++) {
		for (int j = i + 1; j < 4; j++) {
			temp = *(position+(4*i)+j);
			*(position+(4*i)+j) = *(position+(4*j)+i);
			*(position+(4*j)+i) = temp;
		}
	}
}
static void rotate(int* position) {
	flip(position);
	transpose(position);
}
static void rotate4(int* position) {
	rotate(position);
	rotate(position);
	rotate(position);
	rotate(position);
}
void Naive4x4Test(int* position) {
	rotate4(position);
	flip(position);
	rotate4(position);
	flip(position);
}
/*	
static void printMatrix(int* position) {
	for (int i = 0; i < 4; i++) {
		printf("%2d %2d %2d %2d\n", *(position+(4*i)), *(position+(4*i)+1), *(position+(4*i)+2), *(position+(4*i)+3));
	}
}
static int* createTest() {
	int* test = malloc(sizeof(int) * 16);
	for (int i = 0; i < 16; i++) {
		*(test+i) = i;
	}
	return test;
}
int main() {
	int* test = createTest();
	printMatrix(test);
	transpose(test);
	printMatrix(test);
	return 0;
}*/
