#!/bin/sh

python start-clients.py \
-f 11211 \
-u 11211 \
-k 100 \
-t 1 \
-z 135 \
-r 6650 \
-w 350 \
--nb_clients $2 \
--nb_servers $1 \
--nb_core 32 \
--duration 100 \
--server 10.10.2.2

#
#-r 304000 \
x#-w 16000 \

# 10M
# -r 6650 \
# -w 350 \
