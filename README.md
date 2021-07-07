# summer_research_2021

Milestone experiment to speed up network data transmission

<<<<<<< HEAD
Test python socket:
script-server.py and script-client.py
=======

## Description

Run a python server-client data transmission experiment using a python file `$FILE`. `$FILE` can be one of `singlethread-server.py`, `singlethread-client.py`, `multithread-server.py`, `multithread-client.py`


`$CPR` is flag for compression, with 0 indicates no compression on data before transmission, while 1 indicates an application of lz4 compression on testing data. `$num` indicates thread number if `$FILE` is multi-thread program multi-thread; loop number if `$FILE` is a single-thread experiment.

The experiment records the time it takes the client to transmit `$NUM` * 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000 bytes data through a network with TCP, respectively. Each data size is tested 7 times and the average is printed to `experiment1.txt`.
```bash
# Server side
~$ ./script-server.sh $FILE $CPR $NUM

# Client side
~$ ./script-client.sh $FILE $CPR $NUM
```
>>>>>>> f23e6655d50ceb6aca900dde836d707feb884114
