#!/bin/bash
gcc -o sthread-uncps-s ./sthread-uncps-s.c ./parameters.c
PORT=60000
for((data_size=1000; data_size<=100000000; data_size*=10))
do
    for((i=0; i<5; i++))
    do
        ./sthread-uncps-s $PORT $data_size
        let "PORT+=10"
	sleep 1
    done
done
