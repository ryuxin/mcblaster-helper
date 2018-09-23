#!/bin/sh

python start-servers.py \
-p 0 \
-u 11211 \
-t 1 \
--nb_core 16 \
--nb_servers 2
