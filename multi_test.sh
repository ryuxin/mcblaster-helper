#!/bin/sh

python start-clients.py \
-f 11211 \
-u 11211 \
-k 100 \
-t 1 \
-z 135 \
-r 4750 \
-w 250 \
--nb_clients 4 \
--nb_servers 2 \
--nb_core 3 \
--duration 10 \
--server 10.10.2.2
