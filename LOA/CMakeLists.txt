cmake_minimum_required(VERSION 3.14)
project(CSolver C)

set(CMAKE_C_STANDARD 99)

add_executable(CSolver main.c search.c GraphGenerator.c UnionFind.c Kruskal.c Queue.c)