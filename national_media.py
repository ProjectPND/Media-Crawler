#!/usr/bin/python
import scrapy
from scrapy.selector import Selector
import re
import hashlib
import json
from urlparse import urlparse
from w3lib.html import remove_tags, remove_tags_with_content
from scrapy.crawler import CrawlerProcess  # For Testing config
from deteksi import deteksi

with open('config.json', 'r') as f:
	config = json.load(f)

print "================= INDEX MEDIA ======================"
print "Choose your media :"
print config.keys()
print "===================================================="

deteksi = deteksi()

i_config = raw_input("Choose Media: ")

target = config[i_config]					
open("log.txt","w").close()
open("result.json","w").close()

class MainMediaSpider(scrapy.Spider):
	name = 'mainmediaspider'

	def log(self,t):
		file = open('log.txt', 'a')
		t = unicode(t)
		file.write(t)
		file.write('\n')
		file.close()


# ======= START COUNTER SYNOPSIS ============ #

	def synopsis(self, s):
		for x in s:
			if len(x) > 50:
			    return x.replace(' - ', '')
			    break
			else:
			    continue
			break

# ================= END ======================== #

# ============================================== #

	def id_hash(self, u):
		return hashlib.md5(json.dumps(u)).hexdigest()

# ============================================== #

	def start_requests(self):
		urls = target["index"] # Must be array type

		try:
			method = target["method"]
		except KeyError:
			method = "GET"

		for url in urls:
			self.log(url)
			yield scrapy.Request(url=url, method=method, callback=self.parse)

	def parse(self, response):
		try:
			xpath = target["xpath_list"]
			lists = response.xpath(xpath).css(target["list"])
		except KeyError:
			lists = response.css(target["list"])


		for article_list in lists:
			nextUrl = article_list.css(target["link"]).extract_first()
			if nextUrl is not None:
				yield response.follow(nextUrl, self.parseDetail)
				# self.log(nextUrl)
			else:
				pass

	def parseDetail(self, response):
		# self.log(response)

		regex = re.compile(r'[\n\r\t]')

		try:
			xpath = target["xpath_body"]
			body = response.xpath(xpath).css(target["body"])
		except KeyError:
			body = response.css(target["body"])

		tautan = None

		for content in body:
			if tautan != response.url:

				tautan = response.url
				parsed_uri = urlparse(tautan)
				domain = parsed_uri[1]  # from config or url
				kanal = parsed_uri[2].split('/')[1]  # from config or url

				kode = self.id_hash(tautan)

				# self.log(kode)
				judul = ''.join(content.css(target["title"]).css('::text').extract())
				judul = re.sub(regex,'',judul).strip()

				# JPNN not have author / editor
				penulis = deteksi.c_editor(content.css(target["author"]).css('::text').extract(), i_config)

				# isi = response.css(target["content"]).css('::text').extract()
				# isi = response.css(target["content"]).extract() # raw HTML source
				# isi = remove_tags_with_content(isi[0], ('script', ))
				# ==================  START : Testing Remove Script from Content ===================== #
				isi = content.css(target["content"]).extract()
				isi = unicode(''.join(isi))

				try:
					for x in target["r_tag"]:
						r_tag = content.css(x).extract()
						for r in r_tag:
							t = unicode(''.join(r))
							isi = re.sub(t,'',isi)
					# self.log(isi)
				except KeyError:
					pass
				
				isi = remove_tags_with_content(isi, ('script','style' ))
				isi = Selector(text=isi).xpath('//text()').extract()
				# ================== END : Testing Remove Script from Content ===================== #

				sipnosis = self.synopsis(isi)  # get from content target
				sipnosis = re.sub(regex,'',sipnosis).strip()
				isi = ' '.join(isi).split()#.strip()
				isi = ' '.join(isi)

				try:
					r_content = target["r_content"]
					for x in r_content:
						# reg = re.compile(r)
						# isi = re.sub(r'Aktual.com-','',isi)
						try:
							sipnosis = re.sub(x,'',sipnosis)
							isi = re.sub(x,'',isi)
						except TypeError:
							pass
						# isi = isi.replace(x,'')
						# self.log(isi)
				except KeyError:
					pass
				isi = re.sub(regex,'',isi).strip()
				# self.log(isi)

				# isi = unicodedata.normalize('NFKD', unicode(isi))
				# isi = regex.sub('') # For remove character from reg expression
				# isi = re.sub(r"\s+", " ", isi, flags=re.UNICODE) # remove whitespaces to one space

				tanggal = deteksi.c_date(content.css(target["date"]).css('::text').extract(), i_config)
				# self.log(tanggal)

				bahasa = target["lang"]

				yield {'id': kode, 'url': tautan, 'title': judul, 'date': tanggal, 'editor': penulis, 'content': isi, 'synopsis': sipnosis, 'media': domain, 'kanal': kanal, 'lang': bahasa}


# For Testing config with different format

process = CrawlerProcess({
	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	'FEED_FORMAT': 'json',
	'FEED_URI': 'result.json',
	'DOWNLOAD_DELAY' : 0.25
})

process.crawl(MainMediaSpider)
process.start()  # the script will block here until the crawling is finished
