#!/bin/bash
#> experiment1.txt
sum=0
PORT=60000
for((data_size=125; data_size<=125000000; data_size*=10))
do
	for((i=0; i<7; i++))
	do
		sleep 2
		data=$(python3 $1 "$PORT" "$data_size" "$2" "$3" | tail -n 1)
                sum=$(echo "$sum+$data" | bc -l)
		let "PORT+=10"

                #Calculate the average
                if [[ $i -eq 6 ]]
                then
                	echo "scale=6; $sum/7" | bc -l >> experiment1.txt
                fi	
	done
done
