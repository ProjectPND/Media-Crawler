#!/bin/bash

server=http://localhost:9200/
deteksi=deteksi
mapping=.mapping.json

curl -XDELETE $server$deteksi
elasticdump --input=$deteksi$mapping --output=$server$deteksi --type=mapping
