#!/bin/bash
PORT=60000
for file in supplier.tbl region.tbl partsupp.tbl part.tbl orders.tbl nation.tbl lineitem.tbl customer.tbl
do 
	for((i=0; i<=4; i++))
	do	
		sleep 2
		echo "single, uncompressed, ${file}"
		python3 ./sthread-tbl-s.py $PORT $file 0
		let "PORT+=10"
	done
	for((i=0; i<=4; i++))
	do
		sleep 2
		echo "single, compressed, ${file}"
    	python3 ./sthread-tbl-s.py $PORT $file 1
    	let "PORT+=10"
	done
	for((i=0; i<=4; i++))
	do
		sleep 2
		echo "multi, uncompressed, ${file}"
		python3 ./mthread-tbl-s.py $PORT $file 0 1
		let "PORT+=10"
	done
	for((i=0; i<=4; i++))
	do
		sleep 2
		echo "multi, compressed, ${file}"
    	python3 ./mthread-tbl-s.py $PORT $file 1 1
    	let "PORT+=10"
	done
done
