#!/bin/bash
PORT=60000
for((data_size=125; data_size<=12500000; data_size*=10))
do
	sum=0
	for((i=0; i<5; i++))
	do
		data=$(python3 $1 "$PORT" "$data_size" "$2" "$3" | tail -n 1)
		sum=$(echo "$sum+$data" | bc -l)
		let "PORT+=10"
		sleep 4

        #Calculate the average
        if [[ $i -eq 4 ]]
        then
        	echo "scale=6; $sum/5" | bc -l >> $4 #$4 is the file name to store the result
        fi	
	done
done
