#!/bin/bash                                                                                               
PORT=60000                                               
for((thread_num=1; thread_num<=6; thread_num++))                                       
do  
    sum=0                                                          
    for((i=0;i<5;i++))                                  
    do                                                                                             
        data=$(python3 ./mthread-singlecolumn-c.py "$PORT" 1 | tail -n 1)                                              
        sum=$(echo "$sum+$data" | bc -l)
        let "PORT+=10"
        sleep 4

        #Calculate the average
        if [[ $i -eq 4 ]]
        then
        	echo "scale=6; $sum/5" | bc -l >> result4.txt
        fi	                              
    done                                                
done                                                        