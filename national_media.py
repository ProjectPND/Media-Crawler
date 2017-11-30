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
import sys
from datetime import datetime
import os

from stem import Signal
from stem.control import Controller
# import unicodedata

with open('config.json', 'r') as f:
	config = json.load(f)

# print "================= INDEX MEDIA ======================"
# print "Choose your media :"
# print config.keys()
# print "===================================================="

# i_config = raw_input("Choose Media: ")

deteksi = deteksi()

i_config = sys.argv[1]
t_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(' ','_').replace(':','_')

# o_config = 'data/'+i_config+'__'+t_now+'.json'
o_config = 'data/'+i_config+'.json'


target = config[i_config]					
open("log.txt","w").close()
open(o_config,"w").close()

# try:
# 	proxy = target["proxy"]
# 	os.environ["http_proxy"] = proxy
# except KeyError:
# 	pass

try:
	target["mobile"]
	u_agent = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
except KeyError:
	u_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'


def _set_new_ip():
    with Controller.from_port(port=9051) as controller:
        # controller.authenticate(password='tor_password')
        controller.signal(Signal.NEWNYM)

class s_Item(scrapy.Item):
    content = scrapy.Field()

class MainMediaSpider(scrapy.Spider):
	name = 'mainmediaspider'
	handle_httpstatus_list = [301,404,503]

	def log(self,t):
		file = open('log.txt', 'a')
		# t = unicode(t)
		t = deteksi.s_undecode(t)
		file.write(t)
		file.write('\n')
		file.close()


# ======= START COUNTER SYNOPSIS ============ #

	def synopsis(self, s):
		for x in s:
			if len(x) > 50:
			    return x#.replace(' - ', '')
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
			# self.log(url)
			request = scrapy.Request(url=url, method=method, callback=self.parse)
			# try:
			# 	# _set_new_ip()
			# 	# request.meta['proxy'] = 'http://127.0.0.1:9051'
			# 	# proxy = target["proxy"]
			# 	# request.meta['proxy'] = proxy
			# except KeyError:
			# 	pass

			# self.log(request.meta['proxy'])
			yield request

	def parse(self, response):
		try:
			xpath = target["xpath_list"]
			lists = response.xpath(xpath).css(target["list"])
		except KeyError:
			lists = response.css(target["list"])
		# self.log(lists)

		for article_list in lists:
			nextUrl = article_list.css(target["link"]).extract_first()
			if nextUrl is not None:
			# 	request = scrapy.Request(url=nextUrl, callback=self.parseDetail)
			# 	# yield response.follow(nextUrl, self.parseDetail)
				# self.log(nextUrl)
			# 	try:
			# 		proxy = target["proxy"]
			# 		request.meta['proxy'] = proxy
			# 	except KeyError:
			# 		pass

				# yield request
				yield response.follow(nextUrl, self.parseDetail)

			# else:
			# 	pass

	def parseDetail(self, response):
		# self.log(response.status)

		regex = re.compile(r'[\n\r\t]')

		try:
			xpath = target["xpath_body"]
			body = response.xpath(xpath).css(target["body"])
		except KeyError:
			body = response.css(target["body"])

		tautan = None
		# self.log(response.css(".container .news-read .article .chatNews #lifeSocial").extract())


		for content in body:
			if tautan != response.url:

				tautan = response.url
				parsed_uri = urlparse(tautan)
				# domain = parsed_uri[1]  # from config or url
				domain = target['media']  # from config or url
				kanal = target["category"]  # from config or url
				# kanal = parsed_uri[2].split('/')[1]  # from config or url

				kode = self.id_hash(tautan)

				# self.log(content.css("article div.lf-ghost"))
				judul = ''.join(content.css(target["title"]).css('::text').extract())
				judul = re.sub(regex,'',judul).strip()

				# JPNN not have author / editor
				penulis = deteksi.c_editor(content.css(target["author"]).css('::text').extract(), i_config)
				# ==================  START : Testing Remove Script from Content ===================== #

				# if target["paging"] is not None:
				# 	paging = target["paging"]
				# 	p_URL = response.css(paging[0]).extract()[1:-1]
				# 	isi = content.css(target["content"])
				# 	for p in p_URL:
				# 		# c = deteksi.p_content(p,target["content"])
				# 		c = Request(response.urljoin(p),callback=deteksi.p_content, meta={'t_content':target["content"]})
				# 		self.log(c.callback)
				# else :
				# 	isi = content.css(target["content"]).extract()

				try:
					page = target["paging"]
					page = response.css('.pagination a::attr("href")').extract()
					try:
						del page[-1]
						# item = response.meta['item']
						item = s_Item()
						request = scrapy.Request(url=page[0],callback=deteksi.p_link)
						# request = deteksi.p_link(page[0])
						request.meta['item'] = item
						yield request
						
						self.log(item)
						self.log(request.meta['item'])
					except IndexError:
						pass
					# page = deteksi.p_link(scrapy,page,target["content"])
				except KeyError:
					pass


				isi = content.css(target["content"]).extract()
				# self.log(isi)
				try:
					for x in target["r_index"]:
						i = deteksi.f_index(isi,x)
						for li in i:
							del isi[li]
						# self.log(x)
				except KeyError:
					pass

				# isi = unicode(''.join(isi))
				# self.log(isi)
				isi = deteksi.s_undecode(''.join(isi))
				try:
					for x in target["r_tag"]:
						r_tag = content.css(x).extract()
						# self.log(content.css(x))
						for r in r_tag:
							t = unicode(''.join(r))
							# t = t.encode('ascii', 'ignore').decode('unicode_escape')
							t = deteksi.s_undecode(''.join(r)).replace('(','\(').replace(')','\)').replace('/','\/').replace('+','\+')
							# t = re.escape(t)
							# t = re.sub(r'[()]')
							# isi = re.escape(isi)
							isi = re.sub(t,'',isi)
							# isi = deteksi.s_undecode(isi)
							# isi = deteksi.s_undecode(re.escape(t))
							# self.log(t)
							# self.log(isi)
				except KeyError:
					pass
				
				isi = remove_tags_with_content(isi, ('script','style'))
				
				# isi = Selector(text=isi).xpath('//text()').extract()
				# self.log(isi)
				# ================== END : Testing Remove Script from Content ===================== #

				try:
					i_synopsis = target["synopsis"]
					sinopsis = Selector(text=isi).css(target['synopsis']).extract_first()
					sinopsis = Selector(text=sinopsis).xpath('//text()').extract()
					sinopsis = ' '.join(sinopsis)
					isi = Selector(text=isi).xpath('//text()').extract()
				except KeyError:
					isi = Selector(text=isi).xpath('//text()').extract()
					sinopsis = self.synopsis(isi)  # get from content target
				
				try:
					sinopsis = re.sub(regex,'',sinopsis).strip()
				except TypeError:
					pass

				isi = ' '.join(isi).split()#.strip()
				isi = ' '.join(isi)

				try:
					r_content = target["r_content"]
					for x in r_content:
						try:
							sinopsis = re.sub(x,'',sinopsis)
							isi = re.sub(x,'',isi)
						except TypeError:
							pass
				except KeyError:
					pass

				isi = re.sub(regex,'',isi).strip()

				tanggal = deteksi.c_date(content.css(target["date"]).css('::text').extract(), i_config)
				# self.log(tanggal)

				bahasa = target["lang"]

				if isi is not "" :
					yield {'id': kode, 'url': tautan, 'title': judul, 'date': tanggal, 'editor': penulis, 'content': isi, 'synopsis': sinopsis, 'media': domain, 'kanal': kanal, 'lang': bahasa}
					# yield {'id': tes}
				else:
					self.log({'id': kode, 'url': tautan, 'title': judul, 'date': tanggal, 'editor': penulis, 'content': isi, 'synopsis': sinopsis, 'media': domain, 'kanal': kanal, 'lang': bahasa})

# For Testing config with different format

process = CrawlerProcess({
	'USER_AGENT': u_agent,
	# 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
	'FEED_FORMAT': 'json',
	'FEED_URI': o_config,
	'DOWNLOAD_DELAY' : 1.0,
	'AUTOTHROTTLE_ENABLED' : True
})

process.crawl(MainMediaSpider)
process.start()  # the script will block here until the crawling is finished

# s_file = os.stat(o_config).st_size
# if s_file == 0:
# 	open(o_config,"rb").close()
# 	os.remove(o_config)
