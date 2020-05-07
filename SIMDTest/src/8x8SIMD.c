#include <stdio.h>
#include <stdlib.h>
#include <x86intrin.h>
static void flip(int* position){
	__m256i r0,r1,r2,r3,r4,r5,r6,r7;

	r0 = _mm256_load_si256(&position[0*8]);
	r1 = _mm256_load_si256(&position[1*8]);
	r2 = _mm256_load_si256(&position[2*8]);
	r3 = _mm256_load_si256(&position[3*8]);
	r4 = _mm256_load_si256(&position[4*8]);
	r5 = _mm256_load_si256(&position[5*8]);
	r6 = _mm256_load_si256(&position[6*8]);
	r7 = _mm256_load_si256(&position[7*8]);
	
	_mm256_store_si256(&position[0*8],r7);
	_mm256_store_si256(&position[1*8],r6);
	_mm256_store_si256(&position[2*8],r5);
	_mm256_store_si256(&position[3*8],r4);
	_mm256_store_si256(&position[4*8],r3);
	_mm256_store_si256(&position[5*8],r2);
	_mm256_store_si256(&position[6*8],r1);
	_mm256_store_si256(&position[7*8],r0);
}
static void transpose(int* position){
	__m256 r0,r1,r2,r3,r4,r5,r6,r7;
	__m256 t0,t1,t2,t3,t4,t5,t6,t7;
	
	r0 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[0*8+0]))),_mm_castsi128_ps(_mm_load_si128(&position[4*8+0])) ,1);
	r1 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[1*8+0]))),_mm_castsi128_ps(_mm_load_si128(&position[5*8+0])) ,1);
	r2 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[2*8+0]))),_mm_castsi128_ps(_mm_load_si128(&position[6*8+0])) ,1);
	r3 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[3*8+0]))),_mm_castsi128_ps(_mm_load_si128(&position[7*8+0])) ,1);
	r4 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[0*8+4]))),_mm_castsi128_ps(_mm_load_si128(&position[4*8+4])) ,1);
	r5 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[1*8+4]))),_mm_castsi128_ps(_mm_load_si128(&position[5*8+4])) ,1);
	r6 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[2*8+4]))),_mm_castsi128_ps(_mm_load_si128(&position[6*8+4])) ,1);
	r7 = _mm256_insertf128_ps(_mm256_castps128_ps256(_mm_castsi128_ps(_mm_load_si128(&position[3*8+4]))),_mm_castsi128_ps(_mm_load_si128(&position[7*8+4])) ,1);

	t0 = _mm256_unpacklo_ps(r0,r1);
	t1 = _mm256_unpackhi_ps(r0,r1);
	t2 = _mm256_unpacklo_ps(r2,r3);
	t3 = _mm256_unpackhi_ps(r2,r3);
	t4 = _mm256_unpacklo_ps(r4,r5);
	t5 = _mm256_unpackhi_ps(r4,r5);
	t6 = _mm256_unpacklo_ps(r6,r7);
	t7 = _mm256_unpackhi_ps(r6,r7);

	__m256 v;

	v = _mm256_shuffle_ps(t0,t2,0x4E);
	r0 = _mm256_blend_ps(t0,v,0xCC);
	r1 = _mm256_blend_ps(t2,v,0x33);

	
	v = _mm256_shuffle_ps(t1,t3,0x4E);
	r2 = _mm256_blend_ps(t1,v,0xCC);
	r3 = _mm256_blend_ps(t3,v,0x33);

	
	v = _mm256_shuffle_ps(t4,t6,0x4E);
	r4 = _mm256_blend_ps(t4,v,0xCC);
	r5 = _mm256_blend_ps(t6,v,0x33);

	
	v = _mm256_shuffle_ps(t5,t7,0x4E);
	r6 = _mm256_blend_ps(t5,v,0xCC);
	r7 = _mm256_blend_ps(t7,v,0x33);

	_mm256_store_si256(&position[0*8],_mm256_castps_si256(r0));
	_mm256_store_si256(&position[1*8],_mm256_castps_si256(r1));
	_mm256_store_si256(&position[2*8],_mm256_castps_si256(r2));
	_mm256_store_si256(&position[3*8],_mm256_castps_si256(r3));
	_mm256_store_si256(&position[4*8],_mm256_castps_si256(r4));
	_mm256_store_si256(&position[5*8],_mm256_castps_si256(r5));
	_mm256_store_si256(&position[6*8],_mm256_castps_si256(r6));
	_mm256_store_si256(&position[7*8],_mm256_castps_si256(r7));
}
static void rotate(int* position) {
	flip(position);
	transpose(position);
}
static void rotate4(int* position) {
	//printMatrix(position);

	rotate(position);
	//printMatrix(position);

	rotate(position);
	//printMatrix(position);

	rotate(position);
	//printMatrix(position);

	rotate(position);
	//printMatrix(position);
}
void SIMD8x8Test(int* position) {
	rotate4(position);
	flip(position);
	rotate4(position);
	flip(position);
}
/*
static void allTogether(int* position) {
	rotate4(position);
	flip(position);
	rotate4(position);
	flip(position);
	printMatrix(position);
}
static void printMatrix(int* position) {
	for (int i = 0; i < 8; i++) {
		printf("%2d %2d %2d %2d %2d %2d %2d %2d\n",*(position+(8*i)+0),*(position+(8*i)+1),*(position+(8*i)+2),*(position+(8*i)+3),*(position+(8*i)+4),*(position+(8*i)+5),*(position+(8*i)+6),*(position+(8*i)+7));
	}
	printf("\n");
}
static int* createTest() {
	int* test = malloc(sizeof(int) * 64);
	for (int i = 0; i < 64; i++){
		*(test+i) = i;
	}
	return test;
}
int main() {
	int* test = createTest();
	allTogether(test);
	free(test);
	return 0;
}*/
