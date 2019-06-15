gcc -c -fPIC -std=c99 -Im -D_GNU_SOURCE -Wall -pedantic -fopenmp -o foo.o MadgwickAHRS.c
gcc -shared -Wl,-soname,libmad.so -o libmad.so foo.o
