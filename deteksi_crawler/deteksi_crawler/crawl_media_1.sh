#!/bin/bash

cd /home/buyung/deteksi_crawler/deteksi_crawler

NOW=$(date +"%Y-%m-%d_%H_%M_%S")
PATH=$PATH:/usr/local/bin
export PATH

scrapy crawl mainmediaspider -a media='detik' -o data/detik_$NOW.json -t json &
scrapy crawl mainmediaspider -a media='viva' -o data/viva_$NOW.json -t json &
scrapy crawl mainmediaspider -a media='kompas' -o data/kompas_$NOW.json -t json &
scrapy crawl mainmediaspider -a media='kontan' -o data/kontan_$NOW.json -t json &
scrapy crawl mainmediaspider -a media='surabaya.tribunnews' -o data/surabaya.tribunnews_$NOW.json -t json &
