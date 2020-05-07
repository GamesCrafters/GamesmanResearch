objects = main.o HashMap.o solver.o loa.o Kruskal.o Queue.o UnionFind.o
LOA : $(objects)
	cc -o LOA  $(objects)
$(objects) : stdlib.h 
solver.o loa.o : stdint.h
Kruskal.o : math.h
HashMap.o: stdio.h inttypes.h
.PHONY : clean
clean :
	-rm LOA $(objects)
