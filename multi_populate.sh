#!/bin/sh

python start-clients.py \
-g 1 \
-f 11211 \
-u 11211 \
-k 100 \
-t 1 \
-z 135 \
-r 0 \
-w 5000 \
--nb_clients $2 \
--nb_servers $1 \
--nb_core 32 \
--duration 10 \
--server 10.10.2.2
