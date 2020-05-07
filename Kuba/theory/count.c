#include <stdio.h>
#include <math.h>
#include <inttypes.h>
uint64_t factorial(uint64_t n) {
	return ((n == 1) || (n == 0)) ? 1 : n * factorial(n-1); 
}
uint64_t choose(uint64_t n, uint64_t k){
	return (factorial(n)/(factorial(k)*factorial(n-k)));
}
uint64_t count() {
	uint64_t big = 0;
	uint64_t small = 0;
	for (uint64_t r = 7; r < 14; r++) {
		for (uint64_t w = 1; w < 9; w++) {
			small = small+(choose(49,r)*choose(49-r,w));
			printf("%" PRIu64 "\n", small);
		}
	}
	for (uint64_t r = 6; r < 14; r++) {
		for (uint64_t w = 1; w < 9; w++) {
			for (uint64_t b = 1; b < 9; b++) {
				big += (choose(49,r)*choose(49-r,w)*choose(49-r-w,b));
			}
		}
	}
	small = small* 2;
	printf("%" PRIu64 "\n", small);
	printf("%" PRIu64 "\n", big);
	return small+big;
}
int main() {
	uint64_t test;
	test = choose(7,1);
	printf("%" PRIu64 "\n", test);
	uint64_t upperbound = count();
	printf("%" PRIu64 "\n",upperbound);
	return 0;
}
