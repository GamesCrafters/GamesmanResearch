#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int* create4x4Test() {
	int* position = malloc(sizeof(int)*16);
	for (int i = 0; i < 16; i++) {
		*(position+i) = i;
	}
	return position;
}
int* create8x8Test() {
	int* position = malloc(sizeof(int)*64);
	for (int i = 0; i < 64; i++) {
		*(position+i) = i;
	}
	return position;
}
int main() {
	int testSize = 0x7FFFFF;
	int* smallTest = create4x4Test();
	int* largeTest = create8x8Test();
	time_t start, Naive4x4, SIMD4x4, Naive8x8, SIMD8x8;
	start = time(NULL);
	for (int i = 0; i < testSize; i++) {
		Naive4x4Test(smallTest);
	}
	Naive4x4 = time(NULL) - start;
	start = time(NULL);
	for (int i = 0; i < testSize; i++) {
		SIMD4x4Test(smallTest);
	}
	SIMD4x4 = time(NULL) - start;
	start = time(NULL);
	for (int i = 0; i < testSize; i++) {
		Naive8x8Test(largeTest);
	}
	Naive8x8 = time(NULL) - start;
	start = time(NULL);
	for (int i = 0; i < testSize; i++) {
		SIMD8x8Test(largeTest);
	}
	SIMD8x8 = time(NULL) - start;
	free(smallTest);
	free(largeTest);
	printf("4x4 Naive: %ld\n", Naive4x4);
	printf("4x4 SIMD: %ld\n", SIMD4x4);
	printf("8x8 Naive: %ld\n", Naive8x8);
	printf("8x8 SIMD: %ld\n", SIMD8x8);
	return 0;
}

