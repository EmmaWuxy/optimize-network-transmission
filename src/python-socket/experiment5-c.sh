#!/bin/bash
> result5.txt
PORT=60000
for FILE in supplier.tbl region.tbl partsupp.tbl part.tbl orders.tbl nation.tbl lineitem.tbl customer.tbl
do
    for ((thread_num=1; thread_num<=6; thread_num++))
    do
        SUM=0
        echo "${FILE}, multithead, transmit last column in ${thread_num} threads" >> result5.txt
        for((i=0;i<=4;i++))
        do
            sleep 4
            data=$(python3 ./mthread-tbl-c.py $PORT 1 | tee /dev/tty | tail -n 1)
            SUM=$(echo "$SUM+$data" | bc -l)
            let "PORT+=20"

            #Calculate the average
            if [[ $i -eq 4 ]]
            then
                echo "scale=6; $SUM/5" | bc -l >> result5.txt
            fi
        done
    done
done