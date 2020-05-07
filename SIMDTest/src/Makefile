CC	= gcc-9
CCFLAGS = -mavx 
TARGETS = PerformanceTest
OBJECTS = test.o 4x4Naive.o 4x4SIMD.o 8x8Naive.o 8x8SIMD.o
PerformanceTest : $(OBJECTS)
	@$(CC) -w -o $(TARGETS) $(OBJECTS) 
	@echo $(TARGETS) "built successfully"
	@rm -f $(OBJECTS)
	@echo "Cleaned up"
test.o : test.c 
	@$(CC) -w -c test.c
	@echo "Compiled test.c"
4x4Naive.o : 4x4Naive.c
	@$(CC) -w -c 4x4Naive.c
	@echo "Compiled 4x4Naive.c"
4x4SIMD.o : 4x4SIMD.c 
	@$(CC) -w -c 4x4SIMD.c
	@echo "Compiled 4x4SIMD.c"
8x8Naive.o : 8x8Naive.c 
	@$(CC) -w -c 8x8Naive.c
	@echo "Compiled 8x8Naive.c"
8x8SIMD.o : 8x8SIMD.c 
	@$(CC) -w $(CCFLAGS) -c 8x8SIMD.c
	@echo "Compiled 8x8SIMD.c"
.PHONY : clean run
run :
	@make
	@echo "Running Performance Test"
	@./$(TARGETS)
	@rm -f $(TARGETS)
clean :
	@rm -f $(TARGETS) $(OBJECTS)
	@echo "Manual clean successful"
