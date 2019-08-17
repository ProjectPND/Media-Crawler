#!/usr/bin/python
from six.moves.urllib.parse import urljoin

import scrapy
from scrapy.selector import Selector
from scrapy.utils.python import to_native_str
from scrapy_splash import SplashRequest

import re
import hashlib
import json
from urlparse import urlparse
from w3lib.html import remove_tags, remove_tags_with_content
from scrapy.crawler import CrawlerProcess  # For Testing config
import os
import shutil
from datetime import datetime

# import unicodedata
from deteksi import deteksi
from datetime import datetime
import json
import sys


with open('config.json', 'r') as f:
	config = json.load(f)

deteksi = deteksi()

i_config = ''
target = {}

t_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(' ','_').replace(':','_')

# o_config = 'data/'+i_config+'__'+t_now+'.json'
#o_config = 'data/'+i_config+'.json'

try:
	shutil.rmtree('temp')				
except (IOError,OSError):
	pass
				
try:
	# shutil.rmtree('temp')				
	open("log.txt","w").close()
	#open(o_config,"w").close()
except IOError:
	pass

#You can also check it get help for you

if not os.path.isdir('data'):
	os.system('mkdir data')
if not os.path.isdir('temp'):
	os.system('mkdir temp')
	
class MainMediaSpider(scrapy.Spider):
	name = 'mainmediaspider'
	handle_httpstatus_list = [301,404,503,504]

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
		# print self.settings.get('USE_MOBILE')
		print '======================='
		print self.settings.get('media')
		
		i_config = self.settings.get('media')
		target = config[i_config]		

		urls = target["index"] # Must be array type

		try:
			method = target["method"]
		except KeyError:
			method = "GET"

		for url in urls:
			# self.log(url)
			try:
				target["js"]
				request = SplashRequest(url, self.parse,
				endpoint='render.html',
				args={'wait': 0.5},
				)
			except KeyError:
				request = scrapy.Request(url=url, method=method, callback=self.parse)

			# self.log(request.meta['proxy'])
			yield request

	def parse(self, response):
		# handle redirection
		# this is copied/adapted from RedirectMiddleware

		i_config = self.settings.get('media')
		target = config[i_config]		
		
		if response.status >= 300 and response.status < 400:
			# HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
			location = to_native_str(response.headers['location'].decode('latin1'))

			# get the original request
			request = response.request
			# and the URL we got redirected to
			redirected_url = urljoin(request.url, location)

			if response.status in (301, 307) or request.method == 'HEAD':
				redirected = request.replace(url=redirected_url)
				yield redirected
			else:
				redirected = request.replace(url=redirected_url, method='GET', body='')
				redirected.headers.pop('Content-Type', None)
				redirected.headers.pop('Content-Length', None)
				yield redirected
			# ========================================== Function for Testing error 301 ============================================ #

		try:
			xpath = target["xpath_list"]
			lists = response.xpath(xpath).css(target["list"])
		except KeyError:
			lists = response.css(target["list"])
		# self.log(lists)

		for article_list in lists:
			nextUrl = article_list.css(target["link"]).extract_first()
			if nextUrl is not None:
				yield response.follow(nextUrl, self.parseDetail)
				# yield scrapy.Request(url=nextUrl, callback=self.parseDetail)


	def parsePaging(self,response):
		i_config = self.settings.get('media')
		target = config[i_config]		

		f = response.meta['f']
		t_content = target['content']
		# self.log(response.meta)
		return deteksi.p_content(response, t_content, f)

	def parseDetail(self, response):
		i_config = self.settings.get('media')
		target = config[i_config]		

		# handle redirection
		# this is copied/adapted from RedirectMiddleware
		if response.status >= 300 and response.status < 400:

			# HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
			location = to_native_str(response.headers['location'].decode('latin1'))

			# get the original request
			request = response.request
			# and the URL we got redirected to
			redirected_url = urljoin(request.url, location)

			if response.status in (301, 307) or request.method == 'HEAD':
				redirected = request.replace(url=redirected_url)
				yield redirected
			else:
				redirected = request.replace(url=redirected_url, method='GET', body='')
				redirected.headers.pop('Content-Type', None)
				redirected.headers.pop('Content-Length', None)
				yield redirected
			# ========================================== Function for Testing error 301 ============================================ #

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
				# domain = parsed_uri[1]  # from config or url
				domain = target['media']  # from config or url
				kanal = target["category"]  # from config or url
				# kanal = parsed_uri[2].split('/')[1]  # from config or url

				kode = self.id_hash(tautan)
				try:
					os.remove('temp/'+kode+'.txt')
				except (IOError,OSError):
					pass

				judul = ''.join(content.css(target["title"]).css('::text').extract())
				judul = re.sub(regex,'',judul).strip()

				# JPNN not have author / editor
				penulis = deteksi.c_editor(content.css(target["author"]).css('::text').extract(), i_config)
				# ==================  START : Testing Remove Script from Content ===================== #

				isi = content.css(target["content"]).extract()
				# self.log(isi)


				try:
					page = target["paging"]
					page = response.css('.pagination a::attr("href")').extract()
					for x in page:

						try:
							del page[-1]
							request = scrapy.Request(url=x,callback=self.parsePaging,meta={'f': kode})
							yield request
							# self.log(x)
							try:
								isi = open(kode+'.txt', 'r').readlines()
								# self.log(isi)
							except IOError: 
								pass
						except IndexError:
							pass
					# for try finding editor in content with paging
					# penulis = deteksi.c_editor(isi, i_config)

				except KeyError:
					pass


				try:
					for x in target["r_index"]:
						i = deteksi.f_index(isi,x)
						for li in i:
							try:
								deteksi.r_index(isi,x)

							except IndexError:
								pass
				except KeyError:
					pass

				isi = deteksi.s_undecode(''.join(isi))
				try:
					for x in target["r_tag"]:
						r_tag = content.css(x).extract()
						for r in r_tag:
							t = unicode(''.join(r))
							t = deteksi.s_undecode(''.join(r)).replace('(','\(').replace(')','\)').replace('/','\/').replace('+','\+')
							isi = re.sub(t,'',isi)
				except KeyError:
					pass
				
				isi = remove_tags_with_content(isi, ('script','style'))
				
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

				bahasa = target["lang"]

				if isi is not "" :
					yield {'id': kode, 'url': tautan, 'title': judul, 'date': tanggal, 'editor': penulis, 'content': isi, 'synopsis': sinopsis, 'media': domain, 'kanal': kanal, 'lang': bahasa}
				else:
					self.log({'id': kode, 'url': tautan, 'title': judul, 'date': tanggal, 'editor': penulis, 'content': isi, 'synopsis': sinopsis, 'media': domain, 'kanal': kanal, 'lang': bahasa})
