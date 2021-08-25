#!/bin/bash
PORT=60000
for((data_size=125; data_size<=12500000; data_size*=10))
do
	for ((i=0; i<5; i++))
	do
		# $1 is the file name, $2 is flag for compression, $3 is thread number of multithread/ loop number for single thread
		python3 $1 "$PORT" "$data_size" "$2" "$3"
		let "PORT+=10"
		sleep 2
	done
done 	
	
