#!/bin/bash
>result2.txt
for((i=2; i<=6; i++))
do
	echo "compressed, single thread, ${i} loops" >> result2.txt
	./script-np-c.sh ./sthread-np-c.py 1 "$i" result2.txt
	sleep 4 
	echo "compressed, multi-thread, ${i} threads" >> result2.txt
	./script-np-c.sh ./mthread-np-c.py 1 "$i" result2.txt
	sleep 4
done
