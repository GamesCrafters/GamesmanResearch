
static void flip(int* position) {
	int temp; 
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 8; j++) {
			temp = *(position+(8*i)+j);
			*(position+(8*i)+j) = *(position+(8*(7-i))+j);
			*(position+(8*(7-i))+j) = temp;
		}
	}
}
static void transpose(int* position) {
	int temp;
	for (int i = 0; i < 7; i++) {
		for (int j = i + 1; j < 8; j++) {
			temp = *(position+(8*i)+j);
			*(position+(8*i)+j) = *(position+(8*j)+i);
			*(position+(8*j)+i) = temp;
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
void Naive8x8Test(int* position) {
	rotate4(position);
	flip(position);
	rotate4(position);
	flip(position);
}
