# Optimize Network Transmission
2021 Summer research project with Joseph Vinish D'silva at McGill University.  

Milestone experiment to speed up network data transmission for AIDA.

## Description and Usage

#### Experiment 1
Python socket vs. C socket comparison for data of size 3,000, 30,000, 300,000, 3,000,000, 30,000,000, 300,000,000 bytes in np arraies.
Result outputs in result1.txt.
###### For C 
```bash
~$ cd ./src/c-socket
# Server side
~$ ./experiment1-s.sh
# Client side
~$ ./experiment1-c.sh
```
###### For Python
```bash
~$ cd ./src/python-socket
# Server side
~$ ./experiment1-s.sh
# Client side
~$ ./experiment1-c.sh
```
#### Experiment 2
Singlethread vs. Multhithread Python program comparison of size 10,000, 100,000, 1,000,000, 10,000,000 in np arraies for a single thread. Thread number are tested from 1 thread to 5 threads.
Result outputs in result2.txt.
###### With data compression
```bash
~$ cd ./src/python-socket
# Server side
~$ ./experiment2-cps-s.sh
# Client side
~$ ./experiment2-cps-c.sh
```
###### With no data compression
```bash
~$ cd ./src/python-socket
# Server side
~$ ./experiment2-uncps-s.sh
# Client side
~$ ./experiment2-uncps-c.sh
```
#### Experiment 3
Singlethread vs. Multhithread Python program comparison on transmitting tables from TPC-H bechmark with data compression. One thread for each single column for multithreading.
Result outputs in result3.txt.
```bash
~$ cd ./src/python-socket
# Server side
~$ ./experiment3-s.sh
# Client side
~$ ./experiment3-c.sh
```
#### Experiment 4
Transmit each column from TPC-H benchmark tables with different number of threads. From single-thread to 6 threads to observe the effect of multithreading on columnes of different data type and different length.
Result outputs in result4.txt.
```bash
~$ cd ./src/python-socket
# Server side
~$ ./experiment4-s.sh
# Client side
~$ ./experiment4-c.sh
```
#### Experiment 5
Multithreading with one thread for each column vs. Multithreading with one thread for each column plus slicing the last column (text column with long length) into multiple threads. Experiemnt are done to slice the last column from 1 thread to 6 threads.
Result outputs in result5.txt.
```bash
~$ cd ./src/python-socket
# Server side
~$ ./experiment5-s.sh
# Client side
~$ ./experiment5-c.sh
```
