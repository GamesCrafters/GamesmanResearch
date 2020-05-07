#Kuba
In progress
## Background 
[Kuba](http://www.di.fc.ul.pt/~jpn/gv/kuba.htm)

### Goal
My goal is to the create the tighest hash possible 
for any solving of the game

### Overview
The end goal is to create a triple tier hash dictonary
the way at the end the API for this structure
should addPosition(position) lookup(position)
The triple tiered dictonary is comprised of 
three layers. 
**First Layer** - Counts red and returns pointer to correct second layer
**Second Layer** - Counts white and returns point to correct third layer
**Third Layer** - Counts black and returns point to the correct hashmap

As we already have an upperbound on the number of positions in each tier
we have intialized all of the hashmaps with that size and this 
gurantees that our load factor = (n/k) < 1 where n is the number of entries
and k is the number of bucks. 

### Symmerties
We can use symmetries in order to lower the entries in each table. Once, we have
computed the actual tree once we have a precise value of k such that n = k for 
all of the maps. This leads to constant time operations for lookup. 

### Runtime Analysis
 
