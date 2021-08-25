#!/bin/bash
PORT=60000
for((thread_num=1; thread_num<=6; thread_num++))
do
	for((i=0;i<5;i++))
	do
		#$1 be the file name, $2 be the column numbers starts from 0
		python3 ./mthread-singlecolumn-s.py "$PORT" $1 1 "$thread_num" $2
		let "PORT+=10"
		sleep 2
	done
done
