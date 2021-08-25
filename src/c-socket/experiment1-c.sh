#!/bin/bash
gcc -o sthread-uncps-c ./sthread-uncps-c.c ./parameters.c
>result1.txt
PORT=60000
for((data_size=1000; data_size<=100000000; data_size*=10))
do
    sum=0
    for((i=0; i<5; i++))
    do
        data=$(./sthread-uncps-c $PORT $data_size | tail -n 1)
        sum=$(echo "$sum+$data" | bc -l)
        let "PORT+=10"
        sleep 3

        #Calculate the average
        if [[ $i -eq 4 ]]
        then
	        echo "C, $data_size" >> result1.txt
            echo "scale=6; $sum/5" | bc -l >> result1.txt
        fi
    done
done
