#!/bin/bash

server=http://localhost:9200/
deteksi=deteksi
mapping=.mapping.json
data=.data.json

rm $deteksi$mapping
rm $deteksi$data
elasticdump --output=$deteksi$mapping --input=$server$deteksi --type=mapping
elasticdump --output=$deteksi$data --input=$server$deteksi --type=data
