#!/bin/sh

python start-clients.py \
-f 11211 \
-u 11211 \
-k 100 \
-t 1 \
-z 135 \
-r 304000 \
-w 16000 \
--nb_clients $2 \
--nb_servers $1 \
--nb_core 32 \
--duration 10 \
--server 10.10.2.2
