#include <stdlib.h>
//TODO:Finish dehash and add testing
//Trying to redo Dan's Scheme rearranger hash in c
int factorial(int n) {
	if (n == 1) {
		return 1;
	} else {
		return n * factorial(n-1);
	}
}
int choose(int n, int k) {
	return (factorial(n)/(factorial(k)*factorial(n-k)));
}
//Input
int rearranger-ox-positions(int s, int o, int x) {
	return (choose(s,o+x)*choose(o+x,x));
}
int* butfirst(int* position, int s) {
	int newposition[s-1];
	for (int i = 1; i < s;i++) {
		*(newposition+i-1) = *(position+i);
	}
	return newposition;
}
int hash-rearranger-ox-h(int* position, int s, int o, int x) {
	if ((s == o) || (s == x) || ((o == 0)&&(x == 0))){
		return 0;
	} else if (*(position) == 0) {
		return hash-rearranger-ox-h(butfirst(position,s),s-1,o,x);
	} else if (*(position) == 2) {
		return ((x+o) == s ? 0 : rearranger-ox-positions(s-1,o,x))+ hash-rearranger-ox-h(butfirst(position,s),s-1,o-1,x);
	} else {
		return (x+o) == s ? 0 : rearranger-ox-positions(s-1,o,x) + o == 0 ? 0 : rearranger-ox-positions(s-1,o-1,x) + hash-rearranger-ox-h(butfirst(position,s),s-1,o,x-1);
	}
}
int hash-rearranger-ox(int* position) {
	int s = 64; int o = 0; int x =0;
	for(int i = 0; i < 64; i++) {
		if (*(position+i) == 2) {
			o++;
		} else if (*(position+i) == 3) {
			x++;
		}
	}
	return hash-rearranger-ox(position,s,o,x);
}
int* unhash-rearranger-ox(int s, int o, int x, int i) {
	return;
}
//CREDIT: http://gamescrafters.berkeley.edu/software/rearranger.scm
