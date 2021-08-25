#!/bin/bash
for ((i=2; i<=6; i++))
do
	echo "uncompressed, single thread, ${i} loops" 
	./script-np-s.sh ./sthread-np-s.py 0 "$i" 
	sleep 2
	echo "uncompressed, multi-thread, ${i} threads"
	./script-np-s.sh ./mthread-np-s.py 0 "$i"
	sleep 2
done
