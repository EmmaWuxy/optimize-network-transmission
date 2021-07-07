#!/bin/bash
for((i=2; i<=6; i++))
do
	./script-client.sh ./singlethread-client.py 1 "$i"
	sleep 6 
	./script-client.sh ./multithread-client.py 1 "$i"
	sleep 6
done
