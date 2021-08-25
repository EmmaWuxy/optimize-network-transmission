#!/bin/bash
for ((i=2; i<=6; i++))
do
	echo "compressed, single thread, ${i} loops"
	./script-np-s.sh ./sthread-np-s.py 1 "$i" 
	sleep 2
	echo "compressed, multi-thread, ${i} threads"
	./script-np-s.sh ./mthread-np-s.py 1 "$i"
	sleep 2
done
