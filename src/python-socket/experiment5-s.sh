#!/bin/bash
# A script to record the time span for trasnmitting a table with multithreads and to discover the optimal number of threads to slicethe longest string column
PORT=60000
for FILE in supplier.tbl region.tbl partsupp.tbl part.tbl orders.tbl nation.tbl lineitem.tbl customer.tbl
do
	for ((thread_num=1; thread_num<=6; thread_num++))
	do
		for ((i=0; i<=4; i++))
		do
			echo "${FILE}, multithead, transmit last column in ${thread_num} threads"
			python3 ./mthread-tbl-s.py $PORT $FILE 1 $thread_num
			let "PORT+=20"
		done
	done
done
