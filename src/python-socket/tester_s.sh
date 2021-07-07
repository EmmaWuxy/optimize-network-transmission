#!/bin/bash
>experiment1.txt
for ((i=2; i<=6; i++))
do
	echo "compressed, single thread, ${i} loops" >> experiment1.txt
	./script-server.sh ./serialization-server.py 1 "$i" 
	sleep 4
	echo "compressed, multi-thread, ${i} threads" >> experiment1.txt
	./script-server.sh ./multithread-server.py 1 "$i"
	sleep 4
done
