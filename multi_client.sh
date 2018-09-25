#!/bin/bash

#killall netserver

nodes=$1
core=0
total_core=32
fp=11211
dp=11211
for n in `seq $nodes`
do
    taskset -c $((core % total_core)) /users/graceliu/facebook-memcached-old/test/mcblaster/mcblaster \
-t 1 -k 100 -z 135 \
-u $((dp)) -f $((fp)) \
-r 6650 -w 350 \
-d 100 10.10.2.2 > logs/mcb_$((fp)) &

    fp=$((fp+1))
    dp=$((dp+1))
    core=$((core+1))
done
echo “started all client”
