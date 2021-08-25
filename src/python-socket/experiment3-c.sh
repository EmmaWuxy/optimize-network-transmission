#!/bin/bash
>result3.txt
PORT=60000
for file in supplier.tbl region.tbl partsupp.tbl part.tbl orders.tbl nation.tbl lineitem.tbl customer.tbl
do
    SUM=0
    echo "single, uncompressed, ${file}" >> result3.txt
    for((i=0; i<=4; i++))
    do
        sleep 4
        data=$(python3 ./sthread-tbl-c.py $PORT 0 | tee /dev/tty | tail -n 1)
        SUM=$(echo "$SUM+$data" | bc -l)
        let "PORT+=10"
        
        if [[ $i -eq 4 ]]
        then
            echo "scale=6; $SUM/5" | bc -l >> result3.txt
        fi
    done

    SUM=0
    echo "single, compressed, ${file}" >> result3.txt
    for((i=0; i<=4; i++))
    do
        sleep 4
        data=$(python3 ./sthread-tbl-c.py $PORT 1 | tee /dev/tty | tail -n 1)
        SUM=$(echo "$SUM+$data" | bc -l)
        let "PORT+=10"

        if [[ $i -eq 4 ]]
        then
            echo "scale=6; $SUM/5" | bc -l >> result3.txt
        fi
    done

    SUM=0
    echo "multi, uncompressed, ${file}" >> result3.txt
    for((i=0; i<=4; i++))
    do
        sleep 4
        data=$(python3 ./mthread-tbl-c.py $PORT 0 | tee /dev/tty | tail -n 1)
        SUM=$(echo "$SUM+$data" | bc -l)
        let "PORT+=10"
        
        if [[ $i -eq 4 ]]
        then
            echo "scale=6; $SUM/5" | bc -l >> result3.txt
        fi
    done
    
    SUM=0
    echo "multi, compressed, ${file}" >> result3.txt
    for((i=0; i<=4; i++))
    do
        sleep 4
        data=$(python3 ./mthread-tbl-c.py $PORT 1 | tee /dev/tty | tail -n 1)
        SUM=$(echo "$SUM+$data" | bc -l)
        let "PORT+=10"

        if [[ $i -eq 4 ]]
        then
            echo "scale=6; $SUM/5" | bc -l >> result3.txt
        fi
    done
done